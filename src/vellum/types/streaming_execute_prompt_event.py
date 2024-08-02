# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .prompt_output import PromptOutput
from .streaming_prompt_execution_meta import StreamingPromptExecutionMeta


class StreamingExecutePromptEvent(pydantic_v1.BaseModel):
    """
    The data returned for each delta during the prompt execution stream.
    """

    output: PromptOutput
    output_index: int
    execution_id: str
    meta: typing.Optional[StreamingPromptExecutionMeta] = None
    raw: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(default=None)
    """
    The subset of the raw response from the model that the request opted into with `expand_raw`.
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
