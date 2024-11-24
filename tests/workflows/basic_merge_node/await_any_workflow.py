from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.nodes.displayable.merge_node import MergeNode
from vellum.workflows.types.core import MergeBehavior
from vellum.workflows.workflows.base import BaseWorkflow


class AwaitAnyMergeNode(MergeNode):
    class Trigger(MergeNode.Trigger):
        merge_behavior = MergeBehavior.AWAIT_ANY


class FirstPassthroughNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        pass

    def run(self) -> Outputs:
        return self.Outputs()


class SecondPassthroughNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        pass

    def run(self) -> Outputs:
        return self.Outputs()


class FinalPassthroughNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value: str

    def run(self) -> Outputs:
        return self.Outputs(value="output")


class AwaitAnyPassingWorkflow(BaseWorkflow):
    graph = (
        {
            FirstPassthroughNode,
            SecondPassthroughNode,
        }
        >> AwaitAnyMergeNode
        >> FinalPassthroughNode
    )

    class Outputs(BaseWorkflow.Outputs):
        value = FinalPassthroughNode.Outputs.value
