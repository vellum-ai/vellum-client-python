from typing import ClassVar, Generic, Union

from vellum.workflows.errors.types import VellumError
from vellum.workflows.nodes.bases import BaseNode
from vellum.workflows.types.generics import StateType


class BaseErrorNode(BaseNode[StateType], Generic[StateType]):
    """
    Used to raise an error to reject the surrounding Workflow.

    error_source_input_id: Union[str, VellumError] - The error to raise.
    """

    error_source_input_id: ClassVar[Union[str, VellumError]]

    class Outputs(BaseNode.Outputs):
        """
        The outputs of the ErrorNode.

        error: str - The error message
        """
        error: str
