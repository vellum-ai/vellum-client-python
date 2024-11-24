import random

from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.workflows.base import BaseWorkflow


class StartNode(BaseNode):
    class Outputs(BaseOutputs):
        next_value: int

    def run(self) -> Outputs:
        return self.Outputs(next_value=random.randint(0, 100))


class NextNode(BaseNode):
    next_value = StartNode.Outputs.next_value

    class Outputs(BaseOutputs):
        final_value: int

    def run(self) -> Outputs:
        return self.Outputs(final_value=self.next_value + 1)


class RunFromNodeWorkflow(BaseWorkflow):
    graph = StartNode >> NextNode

    class Outputs(BaseOutputs):
        final_value = NextNode.Outputs.final_value
