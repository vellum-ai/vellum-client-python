from typing import ClassVar, Generic

from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.types.core import EntityInputsInterface
from vellum.workflows.types.generics import StateType


class BaseSubworkflowNode(BaseNode[StateType], Generic[StateType]):
    # Inputs that are passed to the Subworkflow
    subworkflow_inputs: ClassVar[EntityInputsInterface] = {}
