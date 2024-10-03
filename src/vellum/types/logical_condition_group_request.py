# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .condition_combinator import ConditionCombinator
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from ..core.pydantic_utilities import update_forward_refs


class LogicalConditionGroupRequest(UniversalBaseModel):
    """
    A higher-order condition that combines one or more basic conditions or other higher-order conditions.
    """

    type: typing.Literal["LOGICAL_CONDITION_GROUP"] = "LOGICAL_CONDITION_GROUP"
    conditions: typing.List["LogicalExpressionRequest"]
    combinator: ConditionCombinator
    negated: bool

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


from .logical_expression_request import LogicalExpressionRequest  # noqa: E402

update_forward_refs(LogicalConditionGroupRequest)