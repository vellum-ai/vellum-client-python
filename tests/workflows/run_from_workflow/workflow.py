import random
from uuid import uuid4

from vellum.workflows.errors.types import WorkflowErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.outputs import BaseOutputs
from vellum.workflows.workflows.base import BaseWorkflow


class StartNode(BaseNode):
    class Outputs(BaseOutputs):
        next_value: int

    def run(self) -> Outputs:
        return self.Outputs(next_value=5)


class NextNode(BaseNode):
    next_value = StartNode.Outputs.next_value

    class Outputs(BaseOutputs):
        final_value: int

    def run(self) -> Outputs:
        delta = random.randint(0, 100)
        if delta > 95:
            raise NodeException("The next value is too high", code=WorkflowErrorCode.PROVIDER_ERROR)

        return self.Outputs(final_value=self.next_value + delta)


store_id = uuid4()


class RunFromPreviousWorkflow(BaseWorkflow):
    graph = StartNode >> NextNode

    class Outputs(BaseOutputs):
        final_value = NextNode.Outputs.final_value
