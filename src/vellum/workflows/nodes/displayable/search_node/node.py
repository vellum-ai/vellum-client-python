from typing import ClassVar

from vellum.workflows.nodes.displayable.bases import BaseSearchNode as BaseSearchNode
from vellum.workflows.types.generics import StateType


class SearchNode(BaseSearchNode[StateType]):
    """
    A SearchNode that outputs the text of the search results concatenated as a single string.

    document_index: Union[UUID, str] - Either the Document Index's UUID or its name.
    query: str - The query to search for.
    options: Optional[SearchRequestOptionsRequest] = None - The request options to use for the search
    request_options: Optional[RequestOptions] = None - The request options to use for the search
    chunk_separator: str = "\n\n#####\n\n" - Used to separate the text of each search result.
    """

    chunk_separator: ClassVar[str] = "\n\n#####\n\n"

    class Outputs(BaseSearchNode.Outputs):
        text: str

    def run(self) -> Outputs:
        results = self._perform_search().results
        text = self.chunk_separator.join([r.text for r in results])
        return self.Outputs(results=results, text=text)
