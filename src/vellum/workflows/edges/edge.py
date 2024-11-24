from typing import TYPE_CHECKING, Any, Type

if TYPE_CHECKING:
    from vellum.workflows.nodes.bases import BaseNode
    from vellum.workflows.ports.port import Port


class Edge:
    def __init__(self, from_port: "Port", to_node: Type["BaseNode"]):
        self.from_port = from_port
        self.to_node = to_node

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Edge):
            return False

        return self.from_port == other.from_port and self.to_node == other.to_node

    def __hash__(self) -> int:
        return hash((self.from_port, self.to_node))

    def __repr__(self) -> str:
        return f"{self.from_port} >> {self.to_node}"
