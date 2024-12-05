from vellum import SearchFiltersRequest, SearchRequestOptionsRequest, SearchResultMergingRequest, SearchWeightsRequest
from vellum.workflows.nodes.displayable import SearchNode

from .most_recent_message import MostRecentMessage


class FAADocumentStore(SearchNode):
    query = MostRecentMessage.Outputs.result
    document_index = "9f13b9d8-5410-48ba-b691-593a4cc681d8"
    options = SearchRequestOptionsRequest(
        limit=8,
        weights=SearchWeightsRequest(semantic_similarity=0.8, keywords=0.2),
        result_merging=SearchResultMergingRequest(enabled=True),
        filters=SearchFiltersRequest(external_ids=None, metadata=None),
    )
    chunk_separator = "\n\n#####\n\n"
