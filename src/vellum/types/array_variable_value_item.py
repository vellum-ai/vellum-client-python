# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

from .error_variable_value import ErrorVariableValue
from .function_call_variable_value import FunctionCallVariableValue
from .image_variable_value import ImageVariableValue
from .json_variable_value import JsonVariableValue
from .number_variable_value import NumberVariableValue
from .string_variable_value import StringVariableValue


class ArrayVariableValueItem_String(StringVariableValue):
    type: typing.Literal["STRING"] = "STRING"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ArrayVariableValueItem_Number(NumberVariableValue):
    type: typing.Literal["NUMBER"] = "NUMBER"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ArrayVariableValueItem_Json(JsonVariableValue):
    type: typing.Literal["JSON"] = "JSON"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ArrayVariableValueItem_Error(ErrorVariableValue):
    type: typing.Literal["ERROR"] = "ERROR"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ArrayVariableValueItem_FunctionCall(FunctionCallVariableValue):
    type: typing.Literal["FUNCTION_CALL"] = "FUNCTION_CALL"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class ArrayVariableValueItem_Image(ImageVariableValue):
    type: typing.Literal["IMAGE"] = "IMAGE"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


ArrayVariableValueItem = typing.Union[
    ArrayVariableValueItem_String,
    ArrayVariableValueItem_Number,
    ArrayVariableValueItem_Json,
    ArrayVariableValueItem_Error,
    ArrayVariableValueItem_FunctionCall,
    ArrayVariableValueItem_Image,
]
