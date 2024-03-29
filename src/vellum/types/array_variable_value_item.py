# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .chat_history_variable_value import ChatHistoryVariableValue
from .error_variable_value import ErrorVariableValue
from .function_call_variable_value import FunctionCallVariableValue
from .json_variable_value import JsonVariableValue
from .number_variable_value import NumberVariableValue
from .search_results_variable_value import SearchResultsVariableValue
from .string_variable_value import StringVariableValue


class ArrayVariableValueItem_String(StringVariableValue):
    type: typing_extensions.Literal["STRING"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ArrayVariableValueItem_Number(NumberVariableValue):
    type: typing_extensions.Literal["NUMBER"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ArrayVariableValueItem_Json(JsonVariableValue):
    type: typing_extensions.Literal["JSON"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ArrayVariableValueItem_ChatHistory(ChatHistoryVariableValue):
    type: typing_extensions.Literal["CHAT_HISTORY"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ArrayVariableValueItem_SearchResults(SearchResultsVariableValue):
    type: typing_extensions.Literal["SEARCH_RESULTS"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ArrayVariableValueItem_Error(ErrorVariableValue):
    type: typing_extensions.Literal["ERROR"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class ArrayVariableValueItem_FunctionCall(FunctionCallVariableValue):
    type: typing_extensions.Literal["FUNCTION_CALL"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


ArrayVariableValueItem = typing.Union[
    ArrayVariableValueItem_String,
    ArrayVariableValueItem_Number,
    ArrayVariableValueItem_Json,
    ArrayVariableValueItem_ChatHistory,
    ArrayVariableValueItem_SearchResults,
    ArrayVariableValueItem_Error,
    ArrayVariableValueItem_FunctionCall,
]
