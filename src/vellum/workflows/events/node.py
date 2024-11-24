from typing import Any, Dict, Generic, Literal, Type, Union

from pydantic import field_serializer

from vellum.core.pydantic_utilities import UniversalBaseModel

from vellum.workflows.errors import VellumError
from vellum.workflows.expressions.accessor import AccessorExpression
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.outputs.base import BaseOutput
from vellum.workflows.references.node import NodeReference
from vellum.workflows.types.generics import OutputsType

from .types import BaseEvent, default_serializer, serialize_type_encoder


class _BaseNodeExecutionBody(UniversalBaseModel):
    node_definition: Type[BaseNode]

    @field_serializer("node_definition")
    def serialize_node_definition(self, node_definition: Type, _info: Any) -> Dict[str, Any]:
        return serialize_type_encoder(node_definition)


class _BaseNodeEvent(BaseEvent):
    body: _BaseNodeExecutionBody

    @property
    def node_definition(self) -> Type[BaseNode]:
        return self.body.node_definition


NodeInputName = Union[NodeReference, AccessorExpression]


class NodeExecutionInitiatedBody(_BaseNodeExecutionBody):
    inputs: Dict[NodeInputName, Any]

    @field_serializer("inputs")
    def serialize_inputs(self, inputs: Dict[NodeInputName, Any], _info: Any) -> Dict[str, Any]:
        return default_serializer({descriptor.name: value for descriptor, value in inputs.items()})


class NodeExecutionInitiatedEvent(_BaseNodeEvent):
    name: Literal["node.execution.initiated"] = "node.execution.initiated"
    body: NodeExecutionInitiatedBody

    @property
    def inputs(self) -> Dict[NodeInputName, Any]:
        return self.body.inputs


class NodeExecutionStreamingBody(_BaseNodeExecutionBody):
    output: BaseOutput

    @field_serializer("output")
    def serialize_output(self, output: BaseOutput, _info: Any) -> Dict[str, Any]:
        return default_serializer(output)


class NodeExecutionStreamingEvent(_BaseNodeEvent):
    name: Literal["node.execution.streaming"] = "node.execution.streaming"
    body: NodeExecutionStreamingBody

    @property
    def output(self) -> BaseOutput:
        return self.body.output


class NodeExecutionFulfilledBody(_BaseNodeExecutionBody, Generic[OutputsType]):
    outputs: OutputsType

    @field_serializer("outputs")
    def serialize_outputs(self, outputs: OutputsType, _info: Any) -> Dict[str, Any]:
        return default_serializer(outputs)


class NodeExecutionFulfilledEvent(_BaseNodeEvent, Generic[OutputsType]):
    name: Literal["node.execution.fulfilled"] = "node.execution.fulfilled"
    body: NodeExecutionFulfilledBody[OutputsType]

    @property
    def outputs(self) -> OutputsType:
        return self.body.outputs


class NodeExecutionRejectedBody(_BaseNodeExecutionBody):
    error: VellumError


class NodeExecutionRejectedEvent(_BaseNodeEvent):
    name: Literal["node.execution.rejected"] = "node.execution.rejected"
    body: NodeExecutionRejectedBody

    @property
    def error(self) -> VellumError:
        return self.body.error


class NodeExecutionPausedBody(_BaseNodeExecutionBody):
    pass


class NodeExecutionPausedEvent(_BaseNodeEvent):
    name: Literal["node.execution.paused"] = "node.execution.paused"
    body: NodeExecutionPausedBody


class NodeExecutionResumedBody(_BaseNodeExecutionBody):
    pass


class NodeExecutionResumedEvent(_BaseNodeEvent):
    name: Literal["node.execution.resumed"] = "node.execution.resumed"
    body: NodeExecutionResumedBody


NodeEvent = Union[
    NodeExecutionInitiatedEvent,
    NodeExecutionStreamingEvent,
    NodeExecutionFulfilledEvent,
    NodeExecutionRejectedEvent,
    NodeExecutionPausedEvent,
    NodeExecutionResumedEvent,
]
