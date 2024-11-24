from datetime import datetime
from enum import Enum
import json
from uuid import UUID, uuid4
from typing import Any, Dict, Literal

from pydantic import Field

from vellum.core.pydantic_utilities import UniversalBaseModel

from vellum.workflows.state.encoder import DefaultStateEncoder
from vellum.workflows.types.utils import datetime_now


class WorkflowEventType(Enum):
    NODE = "NODE"
    WORKFLOW = "WORKFLOW"


def default_datetime_factory() -> datetime:
    """
    Makes it possible to mock the datetime factory for testing.
    """

    return datetime_now()


excluded_modules = {"typing", "builtins"}


def serialize_type_encoder(obj: type) -> Dict[str, Any]:
    return {
        "name": obj.__name__,
        "module": obj.__module__.split("."),
    }


def default_serializer(obj: Any) -> Any:
    return json.loads(
        json.dumps(
            obj,
            cls=DefaultStateEncoder,
        )
    )


class BaseEvent(UniversalBaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=default_datetime_factory)
    api_version: Literal["2024-10-25"] = "2024-10-25"
    trace_id: UUID
    span_id: UUID
