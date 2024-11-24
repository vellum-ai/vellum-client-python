from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes.bases import BaseNode


class OtherNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        final_value = "ignore"


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        final_value = "hello"


class BasicFallbackValues(BaseWorkflow):
    graph = StartNode

    class Outputs(BaseWorkflow.Outputs):
        final_value = OtherNode.Outputs.final_value.coalesce(StartNode.Outputs.final_value)
