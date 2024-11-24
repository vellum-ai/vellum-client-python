from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.outputs.base import BaseOutputs
from vellum.workflows.state.base import BaseState
from vellum.workflows.workflows.base import BaseWorkflow


class Inputs(BaseInputs):
    value: str


class StartNode(BaseNode):
    class Outputs(BaseOutputs):
        value = Inputs.value


class EndNode(BaseNode):
    class Outputs(BaseOutputs):
        value = StartNode.Outputs.value


class BasicPassthroughWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = StartNode >> EndNode

    class Outputs(BaseOutputs):
        value = StartNode.Outputs.value
        cascaded_value = EndNode.Outputs.value
