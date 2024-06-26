# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

from .workflow_output_array import WorkflowOutputArray
from .workflow_output_chat_history import WorkflowOutputChatHistory
from .workflow_output_error import WorkflowOutputError
from .workflow_output_function_call import WorkflowOutputFunctionCall
from .workflow_output_image import WorkflowOutputImage
from .workflow_output_json import WorkflowOutputJson
from .workflow_output_number import WorkflowOutputNumber
from .workflow_output_search_results import WorkflowOutputSearchResults
from .workflow_output_string import WorkflowOutputString


class WorkflowOutput_String(WorkflowOutputString):
    type: typing.Literal["STRING"] = "STRING"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class WorkflowOutput_Number(WorkflowOutputNumber):
    type: typing.Literal["NUMBER"] = "NUMBER"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class WorkflowOutput_Json(WorkflowOutputJson):
    type: typing.Literal["JSON"] = "JSON"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class WorkflowOutput_ChatHistory(WorkflowOutputChatHistory):
    type: typing.Literal["CHAT_HISTORY"] = "CHAT_HISTORY"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class WorkflowOutput_SearchResults(WorkflowOutputSearchResults):
    type: typing.Literal["SEARCH_RESULTS"] = "SEARCH_RESULTS"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class WorkflowOutput_Array(WorkflowOutputArray):
    type: typing.Literal["ARRAY"] = "ARRAY"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class WorkflowOutput_Error(WorkflowOutputError):
    type: typing.Literal["ERROR"] = "ERROR"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class WorkflowOutput_FunctionCall(WorkflowOutputFunctionCall):
    type: typing.Literal["FUNCTION_CALL"] = "FUNCTION_CALL"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


class WorkflowOutput_Image(WorkflowOutputImage):
    type: typing.Literal["IMAGE"] = "IMAGE"

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True
        populate_by_name = True


WorkflowOutput = typing.Union[
    WorkflowOutput_String,
    WorkflowOutput_Number,
    WorkflowOutput_Json,
    WorkflowOutput_ChatHistory,
    WorkflowOutput_SearchResults,
    WorkflowOutput_Array,
    WorkflowOutput_Error,
    WorkflowOutput_FunctionCall,
    WorkflowOutput_Image,
]
