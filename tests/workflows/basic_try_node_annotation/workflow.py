import random

from vellum.workflows import BaseWorkflow
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.nodes.core.try_node import TryNode


@TryNode.wrap()
class FlakyNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value: int

    def run(self) -> Outputs:
        arg = random.randint(0, 10)
        if arg < 5:
            raise Exception("This is a flaky node")
        return self.Outputs(value=arg)


class SimpleTryExample(BaseWorkflow):
    graph = FlakyNode

    class Outputs(BaseWorkflow.Outputs):
        final_value = FlakyNode.Outputs.value.coalesce(FlakyNode.Outputs.error)
