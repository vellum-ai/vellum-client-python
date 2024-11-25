from typing import List

from vellum import VellumValue
from vellum.workflows.nodes.displayable import FinalOutputNode
from vellum.workflows.state import BaseState

from .map_node import MapNode


class FinalOutput(FinalOutputNode[BaseState, List[VellumValue]]):
    class Outputs(FinalOutputNode.Outputs):
        value = MapNode.Outputs.final_output
