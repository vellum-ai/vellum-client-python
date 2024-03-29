# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .search_result_document_request import SearchResultDocumentRequest

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class SearchResultRequest(pydantic.BaseModel):
    text: str = pydantic.Field(description="The text of the chunk that matched the search query.")
    score: float = pydantic.Field(description="A score representing how well the chunk matches the search query.")
    keywords: typing.List[str]
    document: SearchResultDocumentRequest = pydantic.Field(
        description="The document that contains the chunk that matched the search query."
    )

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        json_encoders = {dt.datetime: serialize_datetime}
