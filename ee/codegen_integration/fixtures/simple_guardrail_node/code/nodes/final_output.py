from vellum.workflows.nodes.displayable import FinalOutputNode
from vellum.workflows.state import BaseState


class FinalOutput(FinalOutputNode[BaseState, float]):
    class Outputs(FinalOutputNode.Outputs):
        value = None
