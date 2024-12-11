from vellum.workflows.nodes.displayable import FinalOutputNode
from vellum.workflows.state import BaseState


class FinalOutput(FinalOutputNode[BaseState, str]):
    class Outputs(FinalOutputNode.Outputs):
        value = None
