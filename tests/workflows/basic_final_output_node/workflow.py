from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.displayable.final_output_node import FinalOutputNode
from vellum.workflows.state.base import BaseState
from vellum.workflows.workflows.base import BaseWorkflow


class Inputs(BaseInputs):
    input: str


class BasicFinalOutputNode(FinalOutputNode):
    class Outputs(FinalOutputNode.Outputs):
        value = Inputs.input


class BasicFinalOutputNodeWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = BasicFinalOutputNode

    class Outputs(BaseWorkflow.Outputs):
        value = BasicFinalOutputNode.Outputs.value
