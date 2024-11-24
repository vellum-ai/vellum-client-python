import time

from vellum.workflows import BaseWorkflow
from vellum.workflows.errors.types import VellumErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.state.base import BaseState
from vellum.workflows.types.core import MergeBehavior


class Inputs(BaseInputs):
    sleep: float


class State(BaseState):
    aggregated = False


class FirstNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        alpha: str

    def run(self) -> Outputs:
        return self.Outputs(alpha="hello")


class SecondNode(BaseNode):
    sleep = Inputs.sleep

    class Outputs(BaseNode.Outputs):
        beta: str

    def run(self) -> Outputs:
        if self.sleep:
            # Simulate a node that runs long enough for the first node to always finish first
            time.sleep(self.sleep)
        return self.Outputs(beta="world")


class FinalNode(BaseNode[State]):
    alpha = FirstNode.Outputs.alpha
    beta = SecondNode.Outputs.beta

    class Outputs(BaseNode.Outputs):
        gamma: str

    class Trigger(BaseNode.Trigger):
        merge_behavior = MergeBehavior.AWAIT_ALL

    def run(self) -> Outputs:
        if self.state.aggregated:
            raise NodeException(
                code=VellumErrorCode.INVALID_STATE,
                message="Final Node should have only executed once.",
            )

        self.state.aggregated = True
        return self.Outputs(gamma=f"{self.alpha} {self.beta}")


class BasicAwaitAllWorkflow(BaseWorkflow[Inputs, State]):
    graph = {FirstNode, SecondNode} >> FinalNode

    class Outputs(BaseWorkflow.Outputs):
        final_value = FinalNode.Outputs.gamma
