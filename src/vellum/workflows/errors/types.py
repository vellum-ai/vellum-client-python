from dataclasses import dataclass
from enum import Enum


class VellumErrorCode(Enum):
    INVALID_WORKFLOW = "INVALID_WORKFLOW"
    INVALID_INPUTS = "INVALID_INPUTS"
    INVALID_OUTPUTS = "INVALID_OUTPUTS"
    INVALID_STATE = "INVALID_STATE"
    INVALID_TEMPLATE = "INVALID_TEMPLATE"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    PROVIDER_ERROR = "PROVIDER_ERROR"
    USER_DEFINED_ERROR = "USER_DEFINED_ERROR"
    WORKFLOW_CANCELLED = "WORKFLOW_CANCELLED"


@dataclass(frozen=True)
class VellumError:
    message: str
    code: VellumErrorCode
