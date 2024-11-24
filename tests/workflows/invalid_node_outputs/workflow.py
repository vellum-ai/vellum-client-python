from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes.bases import BaseNode


class InvalidNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        final_value: str

    def run(self) -> Outputs:  # type: ignore[empty-body]
        pass


class InvalidNodeWorkflow(BaseWorkflow):
    graph = InvalidNode

    class Outputs(BaseWorkflow.Outputs):
        final_value = InvalidNode.Outputs.final_value
