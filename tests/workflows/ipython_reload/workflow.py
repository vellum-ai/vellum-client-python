from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.workflows.base import BaseWorkflow


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        middle_value = "Hello"


class EndNode(BaseNode):
    middle_value = StartNode.Outputs.middle_value

    class Outputs(BaseNode.Outputs):
        final_value: str

    def run(self) -> Outputs:
        return self.Outputs(final_value=f"{self.middle_value} world")


class ReloadableWorkflow(BaseWorkflow):
    graph = StartNode >> EndNode

    class Outputs(BaseWorkflow.Outputs):
        final_value = EndNode.Outputs.final_value
