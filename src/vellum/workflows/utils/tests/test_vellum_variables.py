import pytest
from typing import List, Optional

from vellum import ChatMessage, SearchResult

from vellum.workflows.utils.vellum_variables import primitive_type_to_vellum_variable_type


@pytest.mark.parametrize(
    "type_, expected",
    [
        (str, "STRING"),
        (Optional[str], "STRING"),
        (int, "NUMBER"),
        (Optional[int], "NUMBER"),
        (float, "NUMBER"),
        (Optional[float], "NUMBER"),
        (List[ChatMessage], "CHAT_HISTORY"),
        (Optional[List[ChatMessage]], "CHAT_HISTORY"),
        (List[SearchResult], "SEARCH_RESULTS"),
        (Optional[List[SearchResult]], "SEARCH_RESULTS"),
    ],
)
def test_primitive_type_to_vellum_variable_type(type_, expected):
    assert primitive_type_to_vellum_variable_type(type_) == expected