from vellum import SearchFiltersRequest, SearchRequestOptionsRequest, SearchResultMergingRequest, SearchWeightsRequest
from vellum.workflows.nodes.displayable import SearchNode as BaseSearchNode

from ..inputs import Inputs


class SearchNode(BaseSearchNode):
    query = Inputs.query_1
    document_index = "d5beca61-aacb-4b22-a70c-776a1e025aa4"
    options = SearchRequestOptionsRequest(
        limit=8,
        weights=SearchWeightsRequest(semantic_similarity=0.8, keywords=0.2),
        result_merging=SearchResultMergingRequest(enabled=True),
        filters=SearchFiltersRequest(external_ids=None, metadata=None),
    )
    chunk_separator = "\n\n#####\n\n"
