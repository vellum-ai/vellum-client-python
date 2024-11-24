from vellum.workflows import BaseWorkflow
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.state.base import BaseState


class State(BaseState):
    writable_value: int = 1


class StartNode(BaseNode[State]):
    node_value = State.writable_value

    def run(self) -> BaseNode.Outputs:
        self.state.writable_value += 2
        return self.Outputs()


class EndNode(BaseNode):
    node_value = State.writable_value

    class Outputs(BaseOutputs):
        final_value: int

    def run(self) -> Outputs:
        return self.Outputs(final_value=self.node_value)


class BasicStateManagement(BaseWorkflow[BaseInputs, State]):
    graph = StartNode >> EndNode

    class Outputs(BaseOutputs):
        final_value = EndNode.Outputs.final_value
