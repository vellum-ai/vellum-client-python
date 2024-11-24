from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.workflows.base import BaseWorkflow


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = 1


class EndNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        total = StartNode.Execution.count


class BasicExecutionCounterWorkflow(BaseWorkflow):
    graph = StartNode >> EndNode

    class Outputs(BaseWorkflow.Outputs):
        final_value = EndNode.Outputs.total
