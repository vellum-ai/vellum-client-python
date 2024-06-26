# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

from .node_output_compiled_array_value import NodeOutputCompiledArrayValue
from .node_output_compiled_chat_history_value import NodeOutputCompiledChatHistoryValue
from .node_output_compiled_error_value import NodeOutputCompiledErrorValue
from .node_output_compiled_function_call_value import NodeOutputCompiledFunctionCallValue
from .node_output_compiled_json_value import NodeOutputCompiledJsonValue
from .node_output_compiled_number_value import NodeOutputCompiledNumberValue
from .node_output_compiled_search_results_value import NodeOutputCompiledSearchResultsValue
from .node_output_compiled_string_value import NodeOutputCompiledStringValue


class NodeOutputCompiledValue_String(NodeOutputCompiledStringValue):
    type: typing.Literal["STRING"] = "STRING"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class NodeOutputCompiledValue_Number(NodeOutputCompiledNumberValue):
    type: typing.Literal["NUMBER"] = "NUMBER"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class NodeOutputCompiledValue_Json(NodeOutputCompiledJsonValue):
    type: typing.Literal["JSON"] = "JSON"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class NodeOutputCompiledValue_ChatHistory(NodeOutputCompiledChatHistoryValue):
    type: typing.Literal["CHAT_HISTORY"] = "CHAT_HISTORY"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class NodeOutputCompiledValue_SearchResults(NodeOutputCompiledSearchResultsValue):
    type: typing.Literal["SEARCH_RESULTS"] = "SEARCH_RESULTS"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class NodeOutputCompiledValue_Error(NodeOutputCompiledErrorValue):
    type: typing.Literal["ERROR"] = "ERROR"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class NodeOutputCompiledValue_Array(NodeOutputCompiledArrayValue):
    type: typing.Literal["ARRAY"] = "ARRAY"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class NodeOutputCompiledValue_FunctionCall(NodeOutputCompiledFunctionCallValue):
    type: typing.Literal["FUNCTION_CALL"] = "FUNCTION_CALL"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


NodeOutputCompiledValue = typing.Union[
    NodeOutputCompiledValue_String,
    NodeOutputCompiledValue_Number,
    NodeOutputCompiledValue_Json,
    NodeOutputCompiledValue_ChatHistory,
    NodeOutputCompiledValue_SearchResults,
    NodeOutputCompiledValue_Error,
    NodeOutputCompiledValue_Array,
    NodeOutputCompiledValue_FunctionCall,
]
