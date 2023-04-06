# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ..core.datetime_utils import serialize_datetime
from .search_request_options_request import SearchRequestOptionsRequest


class SearchRequestBodyRequest(pydantic.BaseModel):
    index_id: typing.Optional[str] = pydantic.Field(
        description=("The ID of the index to search against. Must provide either this or index_name.\n")
    )
    index_name: typing.Optional[str] = pydantic.Field(
        description=("The name of the index to search against. Must provide either this or index_id.\n")
    )
    query: str = pydantic.Field(description=("The query to search for.\n"))
    options: typing.Optional[SearchRequestOptionsRequest]

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        json_encoders = {dt.datetime: serialize_datetime}
