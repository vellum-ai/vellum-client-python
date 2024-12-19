from typing import TYPE_CHECKING, Any, Optional, Tuple, Type, TypeVar

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

from vellum.workflows.descriptors.base import BaseDescriptor
from vellum.workflows.errors.types import WorkflowErrorCode
from vellum.workflows.exceptions import NodeException

if TYPE_CHECKING:
    from vellum.workflows.nodes.bases.base import BaseNode
    from vellum.workflows.state.base import BaseState

_T = TypeVar("_T")


class NodeReference(BaseDescriptor[_T]):
    def __init__(
        self, *, name: str, types: Tuple[Type[_T], ...], instance: Optional[_T] = None, node_class: Type["BaseNode"]
    ) -> None:
        self._name = name
        self._types = types
        self._instance = instance
        self._node_class = node_class

    @property
    def node_class(self) -> Type["BaseNode"]:
        return self._node_class

    def resolve(self, state: "BaseState") -> _T:
        raise NodeException(
            f"NodeDescriptors cannot be resolved during runtime. Got: {self._name}",
            code=WorkflowErrorCode.INTERNAL_ERROR,
        )

    def __repr__(self) -> str:
        return f"{self._node_class.__qualname__}.{self._name}"

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.is_instance_schema(cls)
