from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes.bases import BaseNode


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        first = "Hello"


class MiddleNode(BaseNode):
    first = StartNode.Outputs.first

    class Outputs(BaseNode.Outputs):
        second: str

    def run(self) -> "MiddleNode.Outputs":
        return self.Outputs(second=f"{self.first}, World!")


class EndNode(BaseNode):
    second = MiddleNode.Outputs.second

    class Outputs(BaseNode.Outputs):
        third: str

    def run(self) -> "EndNode.Outputs":
        return self.Outputs(third=f"{self.second} Today!")


class BasicChainedEdgesWorkflow(BaseWorkflow):
    graph = StartNode >> MiddleNode >> EndNode

    class Outputs(BaseWorkflow.Outputs):
        final_value = EndNode.Outputs.third
