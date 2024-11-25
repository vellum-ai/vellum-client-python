# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations
from ..core.pydantic_utilities import UniversalBaseModel
from .array_vellum_value import ArrayVellumValue
import typing
from .vellum_value import VellumValue
from .workflow_node_result_event_state import WorkflowNodeResultEventState
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic
from ..core.pydantic_utilities import update_forward_refs


class NodeOutputCompiledArrayValue(UniversalBaseModel):
    """
    An output returned by a node that is of type ARRAY.
    """

    type: typing.Literal["ARRAY"] = "ARRAY"
    value: typing.Optional[typing.List[VellumValue]] = None
    node_output_id: str
    state: typing.Optional[WorkflowNodeResultEventState] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow


update_forward_refs(ArrayVellumValue, NodeOutputCompiledArrayValue=NodeOutputCompiledArrayValue)