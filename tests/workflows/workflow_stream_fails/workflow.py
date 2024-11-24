from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes.bases import BaseNode


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        final_value: str

    def run(self) -> Outputs:
        return StartNode.Outputs(final_value="Hello")


class AlwaysFailsWorkflow(BaseWorkflow):
    graph = StartNode

    class Outputs(BaseWorkflow.Outputs):
        final_value = StartNode.Outputs.final_value
