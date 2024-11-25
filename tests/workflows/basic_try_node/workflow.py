import random

from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.nodes.core.try_node.node import TryNode
from vellum.workflows.nodes.displayable.final_output_node import FinalOutputNode


class StartNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value: int

    def run(self) -> Outputs:
        arg = random.randint(0, 10)
        if arg < 5:
            raise Exception("This is a flaky node")
        return self.Outputs(value=arg)


class Subworkflow(BaseWorkflow):
    graph = StartNode

    class Outputs(StartNode.Outputs):
        pass


class TryableNode(TryNode):
    subworkflow = Subworkflow


class CoalesceNode(FinalOutputNode):
    class Outputs(FinalOutputNode.Outputs):
        value = TryableNode.Outputs.value.coalesce(TryableNode.Outputs.error)


class SimpleTryExample(BaseWorkflow):
    graph = TryableNode >> FinalOutputNode

    class Outputs(BaseWorkflow.Outputs):
        final_value = CoalesceNode.Outputs.value
