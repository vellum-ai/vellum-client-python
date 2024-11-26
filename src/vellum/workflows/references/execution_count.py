from typing import TYPE_CHECKING, Type

from vellum.workflows.descriptors.base import BaseDescriptor

if TYPE_CHECKING:
    from vellum.workflows.nodes.bases import BaseNode
    from vellum.workflows.state.base import BaseState


class ExecutionCountReference(BaseDescriptor[int]):

    def __init__(
        self,
        node_class: Type["BaseNode"],
    ) -> None:
        super().__init__(name=f"Execution Count({node_class.__name__})", types=(int,))
        self._node_class = node_class

    def resolve(self, state: "BaseState") -> int:
        return state.meta.node_execution_cache.get_execution_count(self._node_class)

    @property
    def node_class(self) -> Type["BaseNode"]:
        return self._node_class
