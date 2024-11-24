from typing import ClassVar, Union

from vellum.workflows.errors.types import VellumError, VellumErrorCode
from vellum.workflows.exceptions import NodeException
from vellum.workflows.nodes.bases.base import BaseNode


class ErrorNode(BaseNode):
    """
    Used to raise an error to reject the surrounding Workflow.

    error: Union[str, VellumError] - The error to raise.
    """

    error: ClassVar[Union[str, VellumError]]

    def run(self) -> BaseNode.Outputs:
        if isinstance(self.error, str):
            raise NodeException(message=self.error, code=VellumErrorCode.USER_DEFINED_ERROR)
        elif isinstance(self.error, VellumError):
            raise NodeException(message=self.error.message, code=self.error.code)
        else:
            raise NodeException(
                message=f"Error node received an unexpected input type: {self.error.__class__}",
                code=VellumErrorCode.INVALID_INPUTS,
            )
