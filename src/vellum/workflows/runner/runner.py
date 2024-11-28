from collections import defaultdict
from copy import deepcopy
import logging
from queue import Empty, Queue
from threading import Event as ThreadingEvent, Thread
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Any, Dict, Generic, Iterable, Iterator, Optional, Sequence, Set, Type, Union

from vellum.workflows.constants import UNDEF
from vellum.workflows.descriptors.base import BaseDescriptor
from vellum.workflows.edges.edge import Edge
from vellum.workflows.errors import VellumError, VellumErrorCode
from vellum.workflows.events import (
    NodeExecutionFulfilledEvent,
    NodeExecutionInitiatedEvent,
    NodeExecutionRejectedEvent,
    NodeExecutionStreamingEvent,
    WorkflowEvent,
    WorkflowEventStream,
    WorkflowExecutionFulfilledEvent,
    WorkflowExecutionInitiatedEvent,
    WorkflowExecutionRejectedEvent,
    WorkflowExecutionStreamingEvent,
)
from vellum.workflows.events.node import (
    NodeExecutionFulfilledBody,
    NodeExecutionInitiatedBody,
    NodeExecutionRejectedBody,
    NodeExecutionStreamingBody,
)
from vellum.workflows.events.types import BaseEvent, ParentContext, WorkflowParentContext
from vellum.workflows.events.utils import is_terminal_event
from vellum.workflows.events.workflow import (
    WorkflowExecutionFulfilledBody,
    WorkflowExecutionInitiatedBody,
    WorkflowExecutionPausedBody,
    WorkflowExecutionPausedEvent,
    WorkflowExecutionRejectedBody,
    WorkflowExecutionResumedBody,
    WorkflowExecutionResumedEvent,
    WorkflowExecutionStreamingBody,
)
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.outputs.base import BaseOutput
from vellum.workflows.ports.port import Port
from vellum.workflows.references import ExternalInputReference, OutputReference
from vellum.workflows.runner.types import WorkItemEvent
from vellum.workflows.state.base import BaseState
from vellum.workflows.types.generics import OutputsType, StateType, WorkflowInputsType

if TYPE_CHECKING:
    from vellum.workflows import BaseWorkflow

logger = logging.getLogger(__name__)

RunFromNodeArg = Sequence[Type[BaseNode]]
ExternalInputsArg = Dict[ExternalInputReference, Any]
BackgroundThreadItem = Union[BaseState, WorkflowEvent, None]


class WorkflowRunner(Generic[StateType]):
    _entrypoints: Iterable[Type[BaseNode]]

    def __init__(
        self,
        workflow: "BaseWorkflow[WorkflowInputsType, StateType]",
        inputs: Optional[WorkflowInputsType] = None,
        state: Optional[StateType] = None,
        entrypoint_nodes: Optional[RunFromNodeArg] = None,
        external_inputs: Optional[ExternalInputsArg] = None,
        cancel_signal: Optional[ThreadingEvent] = None,
        parent_context: Optional[ParentContext] = None,
    ):
        if state and external_inputs:
            raise ValueError("Can only run a Workflow providing one of state or external inputs, not both")

        self.workflow = workflow
        if entrypoint_nodes:
            if len(list(entrypoint_nodes)) > 1:
                raise ValueError("Cannot resume from multiple nodes")

            # TODO: Support resuming from multiple nodes
            # https://app.shortcut.com/vellum/story/4408
            node = next(iter(entrypoint_nodes))
            if state:
                self._initial_state = state
            else:
                self._initial_state = self.workflow.get_state_at_node(node)
            self._entrypoints = entrypoint_nodes
        elif external_inputs:
            self._initial_state = self.workflow.get_most_recent_state()
            for descriptor, value in external_inputs.items():
                self._initial_state.meta.external_inputs[descriptor] = value

            self._entrypoints = [
                ei.inputs_class.__parent_class__
                for ei in external_inputs
                if issubclass(ei.inputs_class.__parent_class__, BaseNode)
            ]
        else:
            normalized_inputs = deepcopy(inputs) if inputs else self.workflow.get_default_inputs()
            if state:
                self._initial_state = deepcopy(state)
                self._initial_state.meta.workflow_inputs = normalized_inputs
            else:
                self._initial_state = self.workflow.get_default_state(normalized_inputs)
            self._entrypoints = self.workflow.get_entrypoints()

        self._work_item_event_queue: Queue[WorkItemEvent[StateType]] = Queue()
        self._workflow_event_queue: Queue[WorkflowEvent] = Queue()
        self._background_thread_queue: Queue[BackgroundThreadItem] = Queue()
        self._dependencies: Dict[Type[BaseNode], Set[Type[BaseNode]]] = defaultdict(set)
        self._state_forks: Set[StateType] = {self._initial_state}

        self._active_nodes_by_execution_id: Dict[UUID, BaseNode[StateType]] = {}
        self._cancel_signal = cancel_signal
        self._parent_context = parent_context

        setattr(
            self._initial_state,
            "__snapshot_callback__",
            lambda s: self._snapshot_state(s),
        )

    def _snapshot_state(self, state: StateType) -> StateType:
        self.workflow._store.append_state_snapshot(state)
        self._background_thread_queue.put(state)
        return state

    def _emit_event(self, event: WorkflowEvent) -> WorkflowEvent:
        self.workflow._store.append_event(event)
        self._background_thread_queue.put(event)
        return event

    def _run_work_item(self, node: BaseNode[StateType], span_id: UUID) -> None:
        self._work_item_event_queue.put(
            WorkItemEvent(
                node=node,
                event=NodeExecutionInitiatedEvent(
                    trace_id=node.state.meta.trace_id,
                    span_id=span_id,
                    body=NodeExecutionInitiatedBody(
                        node_definition=node.__class__,
                        inputs=node._inputs,
                    ),
                    parent=WorkflowParentContext(
                        span_id=span_id,
                        workflow_definition=self.workflow.__class__,
                        parent=self._parent_context
                    )
                ),
            )
        )

        logger.debug(f"Started running node: {node.__class__.__name__}")

        try:
            node_run_response = node.run()
            ports = node.Ports()
            if not isinstance(node_run_response, (BaseOutputs, Iterator)):
                raise NodeException(
                    message=f"Node {node.__class__.__name__} did not return a valid node run response",
                    code=VellumErrorCode.INVALID_OUTPUTS,
                )

            if isinstance(node_run_response, BaseOutputs):
                if not isinstance(node_run_response, node.Outputs):
                    raise NodeException(
                        message=f"Node {node.__class__.__name__} did not return a valid outputs object",
                        code=VellumErrorCode.INVALID_OUTPUTS,
                    )

                outputs = node_run_response
            else:
                streaming_output_queues: Dict[str, Queue] = {}
                outputs = node.Outputs()

                for output in node_run_response:
                    invoked_ports = output > ports
                    if not output.is_fulfilled:
                        if output.name not in streaming_output_queues:
                            streaming_output_queues[output.name] = Queue()
                            output_descriptor = OutputReference(
                                name=output.name,
                                types=(type(output.delta),),
                                instance=None,
                                outputs_class=node.Outputs,
                            )
                            node.state.meta.node_outputs[output_descriptor] = streaming_output_queues[output.name]
                            self._work_item_event_queue.put(
                                WorkItemEvent(
                                    node=node,
                                    event=NodeExecutionStreamingEvent(
                                        trace_id=node.state.meta.trace_id,
                                        span_id=span_id,
                                        body=NodeExecutionStreamingBody(
                                            node_definition=node.__class__,
                                            output=BaseOutput(name=output.name),
                                        ),
                                        parent=WorkflowParentContext(
                                            span_id=span_id,
                                            workflow_definition=self.workflow.__class__,
                                            parent=self._parent_context
                                        )
                                    ),
                                    invoked_ports=invoked_ports,
                                )
                            )

                        streaming_output_queues[output.name].put(output.delta)
                        self._work_item_event_queue.put(
                            WorkItemEvent(
                                node=node,
                                event=NodeExecutionStreamingEvent(
                                    trace_id=node.state.meta.trace_id,
                                    span_id=span_id,
                                    body=NodeExecutionStreamingBody(
                                        node_definition=node.__class__,
                                        output=output,
                                    ),
                                    parent=WorkflowParentContext(
                                        span_id=span_id,
                                        workflow_definition=self.workflow.__class__,
                                        parent=self._parent_context,
                                    )
                                ),
                                invoked_ports=invoked_ports,
                            )
                        )
                    else:
                        if output.name in streaming_output_queues:
                            streaming_output_queues[output.name].put(UNDEF)

                        setattr(outputs, output.name, output.value)
                        self._work_item_event_queue.put(
                            WorkItemEvent(
                                node=node,
                                event=NodeExecutionStreamingEvent(
                                    trace_id=node.state.meta.trace_id,
                                    span_id=span_id,
                                    body=NodeExecutionStreamingBody(
                                        node_definition=node.__class__,
                                        output=output,
                                    ),
                                    parent=WorkflowParentContext(
                                        span_id=span_id,
                                        workflow_definition=self.workflow.__class__,
                                        parent=self._parent_context,
                                    )
                                ),
                                invoked_ports=invoked_ports,
                            )
                        )

            for descriptor, output_value in outputs:
                node.state.meta.node_outputs[descriptor] = output_value

            invoked_ports = ports(outputs, node.state)
            node.state.meta.node_execution_cache.fulfill_node_execution(node.__class__, span_id)

            self._work_item_event_queue.put(
                WorkItemEvent(
                    node=node,
                    event=NodeExecutionFulfilledEvent(
                        trace_id=node.state.meta.trace_id,
                        span_id=span_id,
                        body=NodeExecutionFulfilledBody(
                            node_definition=node.__class__,
                            outputs=outputs,
                        ),
                        parent=WorkflowParentContext(
                            span_id=span_id,
                            workflow_definition=self.workflow.__class__,
                            parent=self._parent_context,
                        )
                    ),
                    invoked_ports=invoked_ports,
                )
            )
        except NodeException as e:
            self._work_item_event_queue.put(
                WorkItemEvent(
                    node=node,
                    event=NodeExecutionRejectedEvent(
                        trace_id=node.state.meta.trace_id,
                        span_id=span_id,
                        body=NodeExecutionRejectedBody(
                            node_definition=node.__class__,
                            error=e.error,
                        ),
                        parent=WorkflowParentContext(
                            span_id=span_id,
                            workflow_definition=self.workflow.__class__,
                            parent=self._parent_context,
                        )
                    ),
                )
            )
        except Exception as e:
            logger.exception(f"An unexpected error occurred while running node {node.__class__.__name__}")

            self._work_item_event_queue.put(
                WorkItemEvent(
                    node=node,
                    event=NodeExecutionRejectedEvent(
                        trace_id=node.state.meta.trace_id,
                        span_id=span_id,
                        body=NodeExecutionRejectedBody(
                            node_definition=node.__class__,
                            error=VellumError(
                                message=str(e),
                                code=VellumErrorCode.INTERNAL_ERROR,
                            ),
                        ),
                        parent=WorkflowParentContext(
                            span_id=span_id,
                            workflow_definition=self.workflow.__class__,
                            parent=self._parent_context
                        )
                    ),
                )
            )

        logger.debug(f"Finished running node: {node.__class__.__name__}")

    def _handle_invoked_ports(self, state: StateType, ports: Optional[Iterable[Port]]) -> None:
        if not ports:
            return

        for port in ports:
            for edge in port.edges:
                if port.fork_state:
                    next_state = deepcopy(state)
                    self._state_forks.add(next_state)
                else:
                    next_state = state

                self._run_node_if_ready(next_state, edge.to_node, edge)

    def _run_node_if_ready(
        self, state: StateType, node_class: Type[BaseNode], invoked_by: Optional[Edge] = None
    ) -> None:
        with state.__lock__:
            for descriptor in node_class.ExternalInputs:
                if not isinstance(descriptor, ExternalInputReference):
                    continue

                if state.meta.external_inputs.get(descriptor, UNDEF) is UNDEF:
                    state.meta.external_inputs[descriptor] = UNDEF
                    return

            all_deps = self._dependencies[node_class]
            if not node_class.Trigger.should_initiate(state, all_deps, invoked_by):
                return

            node = node_class(state=state, context=self.workflow.context)
            node_span_id = uuid4()
            state.meta.node_execution_cache.initiate_node_execution(node_class, node_span_id)
            self._active_nodes_by_execution_id[node_span_id] = node

            worker_thread = Thread(target=self._run_work_item, kwargs={"node": node, "span_id": node_span_id})
            worker_thread.start()

    def _handle_work_item_event(self, work_item_event: WorkItemEvent[StateType]) -> Optional[VellumError]:
        node = work_item_event.node
        event = work_item_event.event
        invoked_ports = work_item_event.invoked_ports

        if event.name == "node.execution.initiated":
            return None

        if event.name == "node.execution.rejected":
            self._active_nodes_by_execution_id.pop(event.span_id)
            return event.error

        if event.name == "node.execution.streaming":
            for workflow_output_descriptor in self.workflow.Outputs:
                node_output_descriptor = workflow_output_descriptor.instance
                if not isinstance(node_output_descriptor, OutputReference):
                    continue
                if node_output_descriptor.outputs_class != event.node_definition.Outputs:
                    continue
                if node_output_descriptor.name != event.output.name:
                    continue

                self._workflow_event_queue.put(
                    self._stream_workflow_event(
                        BaseOutput(
                            name=workflow_output_descriptor.name,
                            value=event.output.value,
                            delta=event.output.delta,
                        )
                    )
                )

            self._handle_invoked_ports(node.state, invoked_ports)

            return None

        if event.name == "node.execution.fulfilled":
            self._active_nodes_by_execution_id.pop(event.span_id)
            self._handle_invoked_ports(node.state, invoked_ports)

            return None

        raise ValueError(f"Invalid event name: {event.name}")

    def _initiate_workflow_event(self) -> WorkflowExecutionInitiatedEvent:
        return WorkflowExecutionInitiatedEvent(
            trace_id=self._initial_state.meta.trace_id,
            span_id=self._initial_state.meta.span_id,
            body=WorkflowExecutionInitiatedBody(
                workflow_definition=self.workflow.__class__,
                inputs=self._initial_state.meta.workflow_inputs,
            ),
            parent=self._parent_context,
        )

    def _stream_workflow_event(self, output: BaseOutput) -> WorkflowExecutionStreamingEvent:
        return WorkflowExecutionStreamingEvent(
            trace_id=self._initial_state.meta.trace_id,
            span_id=self._initial_state.meta.span_id,
            body=WorkflowExecutionStreamingBody(
                workflow_definition=self.workflow.__class__,
                output=output,
            ),
            parent=self._parent_context
        )

    def _fulfill_workflow_event(self, outputs: OutputsType) -> WorkflowExecutionFulfilledEvent:
        return WorkflowExecutionFulfilledEvent(
            trace_id=self._initial_state.meta.trace_id,
            span_id=self._initial_state.meta.span_id,
            body=WorkflowExecutionFulfilledBody(
                workflow_definition=self.workflow.__class__,
                outputs=outputs,
            ),
            parent=self._parent_context,
        )

    def _reject_workflow_event(self, error: VellumError) -> WorkflowExecutionRejectedEvent:
        return WorkflowExecutionRejectedEvent(
            trace_id=self._initial_state.meta.trace_id,
            span_id=self._initial_state.meta.span_id,
            body=WorkflowExecutionRejectedBody(
                workflow_definition=self.workflow.__class__,
                error=error,
            ),
            parent=self._parent_context,
        )

    def _resume_workflow_event(self) -> WorkflowExecutionResumedEvent:
        return WorkflowExecutionResumedEvent(
            trace_id=self._initial_state.meta.trace_id,
            span_id=self._initial_state.meta.span_id,
            body=WorkflowExecutionResumedBody(
                workflow_definition=self.workflow.__class__,
            ),
        )

    def _pause_workflow_event(self, external_inputs: Iterable[ExternalInputReference]) -> WorkflowExecutionPausedEvent:
        return WorkflowExecutionPausedEvent(
            trace_id=self._initial_state.meta.trace_id,
            span_id=self._initial_state.meta.span_id,
            body=WorkflowExecutionPausedBody(
                workflow_definition=self.workflow.__class__,
                external_inputs=external_inputs,
            ),
            parent=self._parent_context,
        )

    def _stream(self) -> None:
        # TODO: We should likely handle this during initialization
        # https://app.shortcut.com/vellum/story/4327
        if not self._entrypoints:
            self._workflow_event_queue.put(
                self._reject_workflow_event(
                    VellumError(message="No entrypoints defined", code=VellumErrorCode.INVALID_WORKFLOW)
                )
            )
            return

        for edge in self.workflow.get_edges():
            self._dependencies[edge.to_node].add(edge.from_port.node_class)

        for node_cls in self._entrypoints:
            try:
                self._run_node_if_ready(self._initial_state, node_cls)
            except NodeException as e:
                self._workflow_event_queue.put(self._reject_workflow_event(e.error))
                return
            except Exception:
                err_message = f"An unexpected error occurred while initializing node {node_cls.__name__}"
                logger.exception(err_message)
                self._workflow_event_queue.put(
                    self._reject_workflow_event(
                        VellumError(code=VellumErrorCode.INTERNAL_ERROR, message=err_message),
                    )
                )
                return

        rejection_error: Optional[VellumError] = None

        while True:
            if not self._active_nodes_by_execution_id:
                break

            work_item_event = self._work_item_event_queue.get()
            event = work_item_event.event

            self._workflow_event_queue.put(event)

            rejection_error = self._handle_work_item_event(work_item_event)
            if rejection_error:
                break

        # Handle any remaining events
        try:
            while work_item_event := self._work_item_event_queue.get_nowait():
                self._workflow_event_queue.put(work_item_event.event)

                rejection_error = self._handle_work_item_event(work_item_event)
                if rejection_error:
                    break
        except Empty:
            pass

        final_state = self._state_forks.pop()
        for other_state in self._state_forks:
            final_state += other_state

        unresolved_external_inputs = {
            descriptor
            for descriptor, node_input_value in final_state.meta.external_inputs.items()
            if node_input_value is UNDEF
        }
        if unresolved_external_inputs:
            self._workflow_event_queue.put(
                self._pause_workflow_event(unresolved_external_inputs),
            )
            return

        final_state.meta.is_terminated = True
        if rejection_error:
            self._workflow_event_queue.put(self._reject_workflow_event(rejection_error))
            return

        fulfilled_outputs = self.workflow.Outputs()
        for descriptor, value in fulfilled_outputs:
            if isinstance(value, BaseDescriptor):
                setattr(fulfilled_outputs, descriptor.name, value.resolve(final_state))
            elif isinstance(descriptor.instance, BaseDescriptor):
                setattr(fulfilled_outputs, descriptor.name, descriptor.instance.resolve(final_state))

        self._workflow_event_queue.put(self._fulfill_workflow_event(fulfilled_outputs))

    def _run_background_thread(self) -> None:
        state_class = self.workflow.get_state_class()
        while True:
            item = self._background_thread_queue.get()
            if item is None:
                break

            if isinstance(item, state_class):
                for emitter in self.workflow.emitters:
                    emitter.snapshot_state(item)
            elif isinstance(item, BaseEvent):
                for emitter in self.workflow.emitters:
                    emitter.emit_event(item)

    def _run_cancel_thread(self) -> None:
        if not self._cancel_signal:
            return

        self._cancel_signal.wait()
        self._workflow_event_queue.put(
            self._reject_workflow_event(
                VellumError(code=VellumErrorCode.WORKFLOW_CANCELLED, message="Workflow run cancelled")
            )
        )

    def stream(self) -> WorkflowEventStream:
        background_thread = Thread(target=self._run_background_thread)
        background_thread.start()

        if self._cancel_signal:
            cancel_thread = Thread(target=self._run_cancel_thread)
            cancel_thread.start()

        event: WorkflowEvent
        if self._initial_state.meta.is_terminated or self._initial_state.meta.is_terminated is None:
            event = self._initiate_workflow_event()
        else:
            event = self._resume_workflow_event()

        yield self._emit_event(event)
        self._initial_state.meta.is_terminated = False

        # The extra level of indirection prevents the runner from waiting on the caller to consume the event stream
        stream_thread = Thread(target=self._stream)
        stream_thread.start()

        while stream_thread.is_alive():
            try:
                event = self._workflow_event_queue.get(timeout=0.1)
            except Empty:
                continue

            yield self._emit_event(event)

            if is_terminal_event(event):
                break

        try:
            while event := self._workflow_event_queue.get_nowait():
                yield self._emit_event(event)
        except Empty:
            pass

        if not is_terminal_event(event):
            yield self._reject_workflow_event(
                VellumError(
                    code=VellumErrorCode.INTERNAL_ERROR,
                    message="An unexpected error occurred while streaming Workflow events",
                )
            )

        self._background_thread_queue.put(None)
