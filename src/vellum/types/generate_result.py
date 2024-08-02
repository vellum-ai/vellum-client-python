# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .generate_result_data import GenerateResultData
from .generate_result_error import GenerateResultError


class GenerateResult(pydantic_v1.BaseModel):
    data: typing.Optional[GenerateResultData] = pydantic_v1.Field(default=None)
    """
    An object containing the resulting generation. This key will be absent if the LLM provider experienced an error.
    """

    error: typing.Optional[GenerateResultError] = pydantic_v1.Field(default=None)
    """
    An object containing details about the error that occurred. This key will be absent if the LLM provider did not experience an error.
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
