from uuid import UUID
from typing import Any, ClassVar, Dict, Generic, Iterator, List, Optional, Set, Union, cast

from vellum import (
    ChatMessage,
    WorkflowExpandMetaRequest,
    WorkflowOutput,
    WorkflowRequestChatHistoryInputRequest,
    WorkflowRequestInputRequest,
    WorkflowRequestJsonInputRequest,
    WorkflowRequestNumberInputRequest,
    WorkflowRequestStringInputRequest,
)
from vellum.core import RequestOptions

from vellum.workflows.constants import LATEST_RELEASE_TAG, OMIT
from vellum.workflows.errors import VellumErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.bases.base_subworkflow_node.node import BaseSubworkflowNode
from vellum.workflows.outputs.base import BaseOutput
from vellum.workflows.types.generics import StateType


class SubworkflowDeploymentNode(BaseSubworkflowNode[StateType], Generic[StateType]):
    """
    Used to execute a Workflow Deployment.

    subworkflow_inputs: EntityInputsInterface - The inputs for the Subworkflow
    deployment: Union[UUID, str] - Either the Workflow Deployment's UUID or its name.
    release_tag: str = LATEST_RELEASE_TAG - The release tag to use for the Workflow Execution
    external_id: Optional[str] = OMIT - Optionally include a unique identifier for tracking purposes. Must be unique within a given Workflow Deployment.
    expand_meta: Optional[WorkflowExpandMetaRequest] = OMIT - Expandable execution fields to include in the respownse
    metadata: Optional[Dict[str, Optional[Any]]] = OMIT - The metadata to use for the Workflow Execution
    request_options: Optional[RequestOptions] = None - The request options to use for the Workflow Execution
    """

    # Either the Workflow Deployment's UUID or its name.
    deployment: ClassVar[Union[UUID, str]]

    release_tag: str = LATEST_RELEASE_TAG
    external_id: Optional[str] = OMIT

    expand_meta: Optional[WorkflowExpandMetaRequest] = OMIT
    metadata: Optional[Dict[str, Optional[Any]]] = OMIT

    request_options: Optional[RequestOptions] = None

    def _compile_subworkflow_inputs(self) -> List[WorkflowRequestInputRequest]:
        # TODO: We may want to consolidate with prompt deployment input compilation
        # https://app.shortcut.com/vellum/story/4117

        compiled_inputs: List[WorkflowRequestInputRequest] = []

        for input_name, input_value in self.subworkflow_inputs.items():
            if isinstance(input_value, str):
                compiled_inputs.append(
                    WorkflowRequestStringInputRequest(
                        name=input_name,
                        value=input_value,
                    )
                )
            elif isinstance(input_value, list) and all(isinstance(message, ChatMessage) for message in input_value):
                compiled_inputs.append(
                    WorkflowRequestChatHistoryInputRequest(
                        name=input_name,
                        value=cast(List[ChatMessage], input_value),
                    )
                )
            elif isinstance(input_value, dict):
                compiled_inputs.append(
                    WorkflowRequestJsonInputRequest(
                        name=input_name,
                        value=cast(Dict[str, Any], input_value),
                    )
                )
            elif isinstance(input_value, float):
                compiled_inputs.append(
                    WorkflowRequestNumberInputRequest(
                        name=input_name,
                        value=input_value,
                    )
                )
            else:
                raise NodeException(
                    message=f"Unrecognized input type for input '{input_name}'",
                    code=VellumErrorCode.INVALID_INPUTS,
                )

        return compiled_inputs

    def run(self) -> Iterator[BaseOutput]:
        subworkflow_stream = self._context.vellum_client.execute_workflow_stream(
            inputs=self._compile_subworkflow_inputs(),
            workflow_deployment_id=str(self.deployment) if isinstance(self.deployment, UUID) else None,
            workflow_deployment_name=self.deployment if isinstance(self.deployment, str) else None,
            release_tag=self.release_tag,
            external_id=self.external_id,
            event_types=["WORKFLOW"],
            metadata=self.metadata,
            request_options=self.request_options,
        )

        outputs: Optional[List[WorkflowOutput]] = None
        fulfilled_output_names: Set[str] = set()
        for event in subworkflow_stream:
            if event.type != "WORKFLOW":
                continue
            if event.data.state == "INITIATED":
                continue
            elif event.data.state == "STREAMING":
                if event.data.output:
                    if event.data.output.state == "STREAMING":
                        yield BaseOutput(
                            name=event.data.output.name,
                            delta=event.data.output.delta,
                        )
                    elif event.data.output.state == "FULFILLED":
                        yield BaseOutput(
                            name=event.data.output.name,
                            value=event.data.output.value,
                        )
                        fulfilled_output_names.add(event.data.output.name)
            elif event.data.state == "FULFILLED":
                outputs = event.data.outputs
            elif event.data.state == "REJECTED":
                error = event.data.error
                if not error:
                    raise NodeException(
                        message="Expected to receive an error from REJECTED event",
                        code=VellumErrorCode.INTERNAL_ERROR,
                    )
                elif error.code in VellumErrorCode._value2member_map_:
                    raise NodeException(
                        message=error.message,
                        code=VellumErrorCode(error.code),
                    )
                else:
                    raise NodeException(
                        message=error.message,
                        code=VellumErrorCode.INTERNAL_ERROR,
                    )

        if outputs is None:
            raise NodeException(
                message="Expected to receive outputs from Workflow Deployment",
                code=VellumErrorCode.INTERNAL_ERROR,
            )

        # For any outputs somehow in our final fulfilled outputs array,
        # but not fulfilled by the stream.
        for output in outputs:
            if output.name not in fulfilled_output_names:
                yield BaseOutput(
                    name=output.name,
                    value=output.value,
                )
