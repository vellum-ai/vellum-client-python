from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.ports.port import Port
from vellum.workflows.state.base import BaseState
from vellum.workflows.workflows.base import BaseWorkflow


class State(BaseState):
    value: int


class StartNode(BaseNode[State]):
    def run(self) -> BaseNode.Outputs:
        self.state.value = 1
        return self.Outputs()

    class Ports(BaseNode.Ports):
        default = Port(default=True, fork_state=True)


class TopNode(BaseNode[State]):
    def run(self) -> BaseNode.Outputs:
        self.state.value += 1
        return self.Outputs()


class BottomNode(BaseNode[State]):
    def run(self) -> BaseNode.Outputs:
        self.state.value -= 3
        return self.Outputs()


class FinalTopNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = State.value


class FinalBottomNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = State.value


class BasicStateForkingWorkflow(BaseWorkflow[BaseInputs, State]):
    graph = StartNode >> {
        TopNode >> FinalTopNode,
        BottomNode >> FinalBottomNode,
    }

    class Outputs(BaseWorkflow.Outputs):
        top = FinalTopNode.Outputs.value
        bottom = FinalBottomNode.Outputs.value
