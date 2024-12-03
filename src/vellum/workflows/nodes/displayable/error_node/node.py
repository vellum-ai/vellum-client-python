from typing import ClassVar

from vellum.workflows.nodes.displayable.bases import BaseErrorNode as BaseErrorNode
from vellum.workflows.types.generics import StateType


class ErrorNode(BaseErrorNode[StateType]):
    """
    Used to perform a hybrid search against a Document Index in Vellum.

    document_index: Union[UUID, str] - Either the UUID or name of the Vellum Document Index that you'd like to search
        against
    query: str - The query to search for
    options: Optional[SearchRequestOptionsRequest] = None - Runtime configuration for the search
    request_options: Optional[RequestOptions] = None - The request options to use for the search
    chunk_separator: str = "\n\n#####\n\n" - The separator to use when joining the text of each search result
    """

    chunk_separator: ClassVar[str] = "\n\n#####\n\n"

    class Outputs(BaseErrorNode.Outputs):
        """
        The outputs of the ErrorNode.

        value: str - The error message
        """
        value: str

    def run(self) -> Outputs:
        return self.Outputs(error=self.error_source_input_id)
