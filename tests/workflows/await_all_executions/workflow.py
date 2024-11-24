from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.types.core import MergeBehavior
from vellum.workflows.workflows.base import BaseWorkflow


class FirstNode(BaseNode):
    pass


class SecondNode(BaseNode):
    pass


class FinalNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = "Hello, World!"

    class Trigger(BaseNode.Trigger):
        merge_behavior = MergeBehavior.AWAIT_ALL


class AwaitAllExecutionsWorkflow(BaseWorkflow):
    """
    This workflow is used to ensure that a node can AWAIT ALL executions of other nodes,
    even if those other nodes do not emit outputs.
    """

    graph = {FirstNode, SecondNode} >> FinalNode

    class Outputs(BaseWorkflow.Outputs):
        final_value = FinalNode.Outputs.value
