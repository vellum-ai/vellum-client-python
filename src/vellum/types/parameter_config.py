# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

from .boolean_parameter_config import BooleanParameterConfig
from .const_parameter_config import ConstParameterConfig
from .integer_parameter_config import IntegerParameterConfig
from .number_parameter_config import NumberParameterConfig
from .string_parameter_config import StringParameterConfig


class ParameterConfig_Array(ArrayParameterConfig):
    type: typing.Literal["array"] = "array"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ParameterConfig_Object(ObjectParameterConfig):
    type: typing.Literal["object"] = "object"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ParameterConfig_Integer(IntegerParameterConfig):
    type: typing.Literal["integer"] = "integer"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ParameterConfig_Number(NumberParameterConfig):
    type: typing.Literal["number"] = "number"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ParameterConfig_String(StringParameterConfig):
    type: typing.Literal["string"] = "string"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ParameterConfig_Boolean(BooleanParameterConfig):
    type: typing.Literal["boolean"] = "boolean"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ParameterConfig_OneOf(OneOfParameterConfig):
    type: typing.Literal["oneOf"] = "oneOf"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ParameterConfig_Const(ConstParameterConfig):
    type: typing.Literal["const"] = "const"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


ParameterConfig = typing.Union[
    ParameterConfig_Array,
    ParameterConfig_Object,
    ParameterConfig_Integer,
    ParameterConfig_Number,
    ParameterConfig_String,
    ParameterConfig_Boolean,
    ParameterConfig_OneOf,
    ParameterConfig_Const,
]
from .array_parameter_config import ArrayParameterConfig  # noqa: E402
from .object_parameter_config import ObjectParameterConfig  # noqa: E402
from .one_of_parameter_config import OneOfParameterConfig  # noqa: E402

ParameterConfig_Array.update_forward_refs(
    ArrayParameterConfig=ArrayParameterConfig,
    ObjectParameterConfig=ObjectParameterConfig,
    OneOfParameterConfig=OneOfParameterConfig,
    ParameterConfig=ParameterConfig,
)
ParameterConfig_Object.update_forward_refs(
    ArrayParameterConfig=ArrayParameterConfig,
    ObjectParameterConfig=ObjectParameterConfig,
    OneOfParameterConfig=OneOfParameterConfig,
    ParameterConfig=ParameterConfig,
)
ParameterConfig_OneOf.update_forward_refs(
    ArrayParameterConfig=ArrayParameterConfig,
    ObjectParameterConfig=ObjectParameterConfig,
    OneOfParameterConfig=OneOfParameterConfig,
    ParameterConfig=ParameterConfig,
)
