from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.nodes.displayable.final_output_node import FinalOutputNode
from vellum.workflows.state.base import BaseState
from vellum.workflows.workflows.base import BaseWorkflow


class Inputs(BaseInputs):
    alpha: str
    beta: str


class PassthroughNode(BaseNode):
    pass


class FirstFinalOutputNode(FinalOutputNode):
    class Outputs(FinalOutputNode.Outputs):
        value = Inputs.alpha


class SecondFinalOutputNode(FinalOutputNode):
    class Outputs(FinalOutputNode.Outputs):
        value = Inputs.beta


class MissingWorkflowOutputWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = PassthroughNode >> {FirstFinalOutputNode, SecondFinalOutputNode}

    class Outputs(BaseWorkflow.Outputs):
        alpha = FirstFinalOutputNode.Outputs.value
