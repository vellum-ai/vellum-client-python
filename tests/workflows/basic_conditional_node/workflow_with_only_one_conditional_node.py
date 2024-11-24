from typing import Type

from vellum.workflows import BaseWorkflow
from vellum.workflows.descriptors.base import BaseDescriptor
from vellum.workflows.inputs import BaseInputs
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.nodes.displayable import ConditionalNode
from vellum.workflows.ports import Port
from vellum.workflows.state import BaseState


class Inputs(BaseInputs):
    text: str


def create_simple_workflow(condition_cls: BaseDescriptor) -> Type[BaseWorkflow]:

    class SimpleConditionalPassthroughNode(BaseNode):
        class Outputs(BaseNode.Outputs):
            text_str = Inputs.text

    class SimpleConditionalNode(ConditionalNode):
        class Ports(ConditionalNode.Ports):
            text_str = Port.on_if(condition_cls)
            text_fallthrough = Port.on_else()

    class SimpleFallthroughPassthroughNode(BaseNode):
        class Outputs(BaseNode.Outputs):
            fallthrough = Inputs.text

    class SimpleConditionalWorkflow(BaseWorkflow[Inputs, BaseState]):
        graph = {
            SimpleConditionalNode.Ports.text_str >> SimpleConditionalPassthroughNode,
            SimpleConditionalNode.Ports.text_fallthrough >> SimpleFallthroughPassthroughNode,
        }

        class Outputs(BaseWorkflow.Outputs):
            text = SimpleConditionalPassthroughNode.Outputs.text_str

    return SimpleConditionalWorkflow
