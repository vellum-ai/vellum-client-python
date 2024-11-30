from vellum import SearchFiltersRequest, SearchRequestOptionsRequest, SearchResultMergingRequest, SearchWeightsRequest
from vellum.workflows.nodes.displayable import SearchNode as BaseSearchNode

from ....nodes.map_node.inputs import Inputs


class SearchNode(BaseSearchNode):
    query = Inputs.items
    document_index = "bb9a427f-23d4-4dc6-bd41-ad2b83727171"
    options = SearchRequestOptionsRequest(
        limit=8,
        weights=SearchWeightsRequest(semantic_similarity=0.8, keywords=0.2),
        result_merging=SearchResultMergingRequest(enabled=True),
        filters=SearchFiltersRequest(external_ids=None, metadata=None),
    )
    chunk_separator = "\n\n#####\n\n"
