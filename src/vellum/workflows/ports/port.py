from typing import TYPE_CHECKING, Any, Iterator, List, Optional, Type

from vellum.workflows.descriptors.base import BaseDescriptor
from vellum.workflows.edges.edge import Edge
from vellum.workflows.graph import Graph, GraphTarget
from vellum.workflows.state.base import BaseState
from vellum.workflows.types.core import ConditionType

if TYPE_CHECKING:
    from vellum.workflows.nodes.bases import BaseNode


class Port:
    node_class: Type["BaseNode"]

    _edges: List[Edge]
    _condition: Optional[BaseDescriptor]
    _condition_type: Optional[ConditionType]

    def __init__(
        self,
        default: bool = False,
        fork_state: bool = False,
        condition: Optional[Any] = None,
        condition_type: Optional[ConditionType] = None,
    ):
        self.default = default
        self.node_class = None  # type: ignore[assignment]
        self._fork_state = fork_state
        self._edges = []
        self._condition: Optional[BaseDescriptor] = condition
        self._condition_type: Optional[ConditionType] = condition_type

    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"{self.node_class}.Ports.{self.name}"

    @property
    def fork_state(self) -> bool:
        return self._fork_state

    @property
    def edges(self) -> Iterator[Edge]:
        return iter(self._edges)

    def __rshift__(self, other: GraphTarget) -> Graph:
        if isinstance(other, set) or isinstance(other, Graph):
            return Graph.from_port(self) >> other

        edge = Edge(from_port=self, to_node=other)
        if edge not in self._edges:
            self._edges.append(edge)

        return Graph.from_edge(edge)

    @staticmethod
    def on_if(condition: BaseDescriptor, fork_state: bool = False) -> "Port":
        return Port(condition=condition, condition_type=ConditionType.IF, fork_state=fork_state)

    @staticmethod
    def on_elif(condition: BaseDescriptor, fork_state: bool = False) -> "Port":
        return Port(condition=condition, condition_type=ConditionType.ELIF, fork_state=fork_state)

    @staticmethod
    def on_else(fork_state: bool = False) -> "Port":
        return Port(condition_type=ConditionType.ELSE, fork_state=fork_state)

    def resolve_condition(self, state: BaseState) -> bool:
        if self._condition is None:
            return False

        value = self._condition.resolve(state)
        return bool(value)
