from vellum.workflows.nodes.displayable import InlineSubworkflowNode

from .workflow import SubworkflowNodeWorkflow


class SubworkflowNode(InlineSubworkflowNode):
    subworkflow = SubworkflowNodeWorkflow

    class Outputs(InlineSubworkflowNode.Outputs):
        final_output_1 = SubworkflowNodeWorkflow.Outputs.final_output_1
