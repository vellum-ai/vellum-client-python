from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState

from .inputs import Inputs
from .nodes.error_node import ErrorNode


class Workflow(BaseWorkflow[Inputs, BaseState]):
    graph = ErrorNode
