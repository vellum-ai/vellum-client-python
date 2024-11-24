from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.ports.port import Port
from vellum.workflows.types.core import MergeBehavior
from vellum.workflows.workflows.base import BaseWorkflow


class StartNode(BaseNode):
    pass


class TopNode(BaseNode):
    pass


class BottomNode(BaseNode):
    pass


class LoopNode(BaseNode):
    class Ports(BaseNode.Ports):
        loop = Port.on_if(StartNode.Execution.count.less_than(3))
        end = Port.on_else()

    class Trigger(BaseNode.Trigger):
        merge_behavior = MergeBehavior.AWAIT_ALL


class EndNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        value = LoopNode.Execution.count


class AwaitAllWithLoopsWorkflow(BaseWorkflow):
    """
    This workflow ensures that we can AWAIT ALL executions of multiple nodes,
    even if those nodes are inside of loops.
    """

    graph = (
        StartNode
        >> {
            TopNode,
            BottomNode,
        }
        >> {
            LoopNode.Ports.loop >> StartNode,
            LoopNode.Ports.end >> EndNode,
        }
    )

    class Outputs(BaseWorkflow.Outputs):
        final_value = EndNode.Outputs.value
