# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .array_parameter_config import ArrayParameterConfig
from .integer_parameter_config import IntegerParameterConfig
from .number_parameter_config import NumberParameterConfig
from .object_parameter_config import ObjectParameterConfig
from .parameter_config import ParameterConfig


class MlModelParameterConfig(pydantic_v1.BaseModel):
    temperature: typing.Optional[NumberParameterConfig] = None
    max_tokens: typing.Optional[IntegerParameterConfig] = None
    stop: typing.Optional[ArrayParameterConfig] = None
    top_p: typing.Optional[NumberParameterConfig] = None
    top_k: typing.Optional[IntegerParameterConfig] = None
    frequency_penalty: typing.Optional[NumberParameterConfig] = None
    presence_penalty: typing.Optional[NumberParameterConfig] = None
    logit_bias: typing.Optional[ObjectParameterConfig] = None
    custom_parameters: typing.Optional[typing.Dict[str, typing.Optional[ParameterConfig]]] = None

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