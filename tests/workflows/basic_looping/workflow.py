from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.ports.port import Port
from vellum.workflows.references import LazyReference
from vellum.workflows.state.base import BaseState
from vellum.workflows.workflows.base import BaseWorkflow


class State(BaseState):
    counter = 1


class StartNode(BaseNode[State]):
    counter = LazyReference(lambda: StartNode.Outputs.final_value.coalesce(State.counter))

    class Outputs(BaseNode.Outputs):
        final_value: int

    def run(self) -> Outputs:
        final_value = self.counter + self.state.counter
        self.state.counter = self.counter
        return self.Outputs(final_value=final_value)


class LoopNode(BaseNode):
    class Ports(BaseNode.Ports):
        loop = Port.on_if(StartNode.Outputs.final_value.less_than(10))
        exit = Port.on_else()


class ExitNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        final_value = StartNode.Outputs.final_value


class BasicLoopingWorkflow(BaseWorkflow[BaseInputs, State]):
    graph = StartNode >> {
        LoopNode.Ports.loop >> StartNode,
        LoopNode.Ports.exit >> ExitNode,
    }

    class Outputs(BaseWorkflow.Outputs):
        final_value = ExitNode.Outputs.final_value
        node_execution_count = StartNode.Execution.count
