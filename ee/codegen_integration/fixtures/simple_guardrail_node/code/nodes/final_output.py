from vellum.workflows.nodes.displayable import FinalOutputNode
from vellum.workflows.state import BaseState

from .guardrail_node import GuardrailNode


class FinalOutput(FinalOutputNode[BaseState, float]):
    class Outputs(FinalOutputNode.Outputs):
        value = GuardrailNode.Outputs.score
