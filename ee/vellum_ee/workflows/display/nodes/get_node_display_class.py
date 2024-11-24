from typing import Optional, Type

from vellum_ee.workflows.display.types import NodeDisplayType
from vellum.workflows.types.generics import NodeType


def get_node_display_class(
    base_class: Type[NodeDisplayType], node_class: Type[NodeType], root_node_class: Optional[Type[NodeType]] = None
) -> Type[NodeDisplayType]:
    try:
        node_display_class = base_class.get_from_node_display_registry(node_class)
    except KeyError:
        try:
            return get_node_display_class(
                base_class, node_class.__bases__[0], node_class if root_node_class is None else root_node_class
            )
        except IndexError:
            return base_class

    if not issubclass(node_display_class, base_class):
        raise TypeError(
            f"Expected to find a subclass of '{base_class.__name__}' for node class '{node_class.__name__}'"
        )

    return node_display_class
