# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import typing

import typing_extensions

from .fulfilled_function_call import FulfilledFunctionCall
from .rejected_function_call import RejectedFunctionCall


class FunctionCall_Fulfilled(FulfilledFunctionCall):
    state: typing_extensions.Literal["FULFILLED"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


class FunctionCall_Rejected(RejectedFunctionCall):
    state: typing_extensions.Literal["REJECTED"]

    class Config:
        frozen = True
        smart_union = True
        allow_population_by_field_name = True


FunctionCall = typing.Union[FunctionCall_Fulfilled, FunctionCall_Rejected]
