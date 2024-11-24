from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.ports.port import Port
from vellum.workflows.state.base import BaseState
from vellum.workflows.workflows.base import BaseWorkflow


class Inputs(BaseInputs):
    value: bool


class StartNode(BaseNode):
    class Ports:
        branch_a = Port.on_if(Inputs.value)
        branch_b = Port.on_else()


class BranchANode(BaseNode):
    class Outputs(BaseOutputs):
        final_value: str

    def run(self) -> Outputs:
        return self.Outputs(final_value="Branch A")


class BranchBNode(BaseNode):
    class Outputs(BaseOutputs):
        final_value: str

    def run(self) -> Outputs:
        return self.Outputs(final_value="Branch B")


class BasicConditionalBranchWorkflow(BaseWorkflow[Inputs, BaseState]):
    graph = {
        StartNode.Ports.branch_a >> BranchANode,
        StartNode.Ports.branch_b >> BranchBNode,
    }

    class Outputs(BaseOutputs):
        branch_a = BranchANode.Outputs.final_value
        branch_b = BranchBNode.Outputs.final_value
