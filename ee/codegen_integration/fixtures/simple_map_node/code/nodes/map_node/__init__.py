from vellum.workflows.nodes.displayable import MapNode as BaseMapNode

from ...inputs import Inputs
from .workflow import MapNodeWorkflow


class MapNode(BaseMapNode):
    items = Inputs.items_1
    subworkflow = MapNodeWorkflow
    concurrency = 4

    class Outputs(BaseMapNode.Outputs):
        final_output = MapNodeWorkflow.Outputs.final_output
