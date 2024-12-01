from vellum.workflows.nodes.displayable import FinalOutputNode
from vellum.workflows.state import BaseState
from vellum.workflows.types import Json

from .map_node import MapNode


class FinalOutput(FinalOutputNode[BaseState, Json]):
    class Outputs(FinalOutputNode.Outputs):
        value = MapNode.Outputs.final_output
