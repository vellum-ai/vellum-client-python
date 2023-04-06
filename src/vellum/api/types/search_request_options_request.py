# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .search_result_merging_request import SearchResultMergingRequest
from .search_weights_request import SearchWeightsRequest


class SearchRequestOptionsRequest(pydantic.BaseModel):
    limit: typing.Optional[int] = pydantic.Field(description=("The maximum number of results to return.\n"))
    weights: typing.Optional[SearchWeightsRequest]
    result_merging: typing.Optional[SearchResultMergingRequest]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
