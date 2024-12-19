from typing import TYPE_CHECKING, TypeVar, cast

from vellum.workflows.descriptors.base import BaseDescriptor
from vellum.workflows.errors.types import WorkflowErrorCode
from vellum.workflows.exceptions import NodeException

if TYPE_CHECKING:
    from vellum.workflows.state.base import BaseState


_T = TypeVar("_T")


class StateValueReference(BaseDescriptor[_T]):

    def resolve(self, state: "BaseState") -> _T:
        if hasattr(state, self._name):
            return cast(_T, getattr(state, self._name))

        if state.meta.parent:
            return self.resolve(state.meta.parent)

        raise NodeException(f"Missing required Workflow state: {self._name}", code=WorkflowErrorCode.INVALID_STATE)
