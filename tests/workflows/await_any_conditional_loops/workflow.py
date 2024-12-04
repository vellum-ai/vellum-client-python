from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.ports.port import Port
from vellum.workflows.types.core import MergeBehavior
from vellum.workflows.workflows.base import BaseWorkflow


class StartNode(BaseNode):
    pass


class TopNode(BaseNode):
    class Ports(BaseNode.Ports):
        success = Port.on_if(StartNode.Execution.count.equals(1))
        failure = Port.on_else()


class TopSuccessNode(BaseNode):
    pass


class TopDeadEndNode(BaseNode):
    pass


class BottomNode(BaseNode):
    class Ports(BaseNode.Ports):
        success = Port.on_if(StartNode.Execution.count.equals(2))
        failure = Port.on_else()


class BottomSuccessNode(BaseNode):
    pass


class BottomDeadEndNode(BaseNode):
    pass


class MergeNode(BaseNode):
    class Trigger(BaseNode.Trigger):
        merge_behavior = MergeBehavior.AWAIT_ANY


class LoopNode(BaseNode):
    class Ports(BaseNode.Ports):
        loop = Port.on_if(MergeNode.Execution.count.equals(1))
        exit = Port.on_else()


class ExitNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        final_value = LoopNode.Execution.count


class AwaitAnyWithConditionalLoopsWorkflow(BaseWorkflow):
    r"""
    This is a trickier example of the AWAIT_ANY merge behavior.

    Here's the Ascii diagram:

                     TopDeadEndNode
                     /
              TopNode                       StartNode
             /       \                     /
    StartNode         MergeNode >> LoopNode
            \       /                      \ 
            BottomNode                      ExitNode
                     \ 
                    BottomDeadEndNode
    
    On the first iteration, the TopNode will complete and invoke the MergeNode, the BottomNode will deadend.
    On the second iteration, the BottomNode will complete and invoke the MergeNode, the TopNode will deadend.

    In the perspective of the MergeNode, it will complete once either the TopNode or the BottomNode complete. It
    has no way of knowing whether the invocation of BottomNode was during the first or second iteration.
    """

    graph = StartNode >> {
        TopNode.Ports.failure >> TopDeadEndNode,
        {
            TopNode.Ports.success >> TopSuccessNode,
            BottomNode.Ports.success >> BottomSuccessNode,
        }
        >> MergeNode
        >> {
            LoopNode.Ports.loop >> StartNode,
            LoopNode.Ports.exit >> ExitNode,
        },
        BottomNode.Ports.failure >> BottomDeadEndNode,
    }

    class Outputs(BaseWorkflow.Outputs):
        final_value = ExitNode.Outputs.final_value
