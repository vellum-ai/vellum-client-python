from collections import Counter
from typing import List

from vellum.workflows.ports.port import Port
from vellum.workflows.types.core import ConditionType

PORT_TYPE_PRIORITIES = {
    ConditionType.IF: 1,
    ConditionType.ELIF: 2,
    ConditionType.ELSE: 3,
}


def validate_ports(ports: List[Port]) -> bool:
    # We don't want to validate ports with no condition (default ports)
    port_types = [port._condition_type for port in ports if port._condition_type is not None]
    sorted_port_types = sorted(port_types, key=lambda port_type: PORT_TYPE_PRIORITIES[port_type])

    if sorted_port_types != port_types:
        raise ValueError("Port conditions must be in the following order: on_if, on_elif, on_else")

    counter = Counter(port_types)
    number_of_if_ports = counter[ConditionType.IF]
    number_of_elif_ports = counter[ConditionType.ELIF]
    number_of_else_ports = counter[ConditionType.ELSE]
    ports_class = f"{ports[0].node_class}.Ports"

    if number_of_if_ports == 0 and (number_of_elif_ports > 0 or number_of_else_ports > 0):
        raise ValueError(
            f"Class {ports_class} containing on_elif or on_else port conditions must have at least one on_if condition"
        )

    if number_of_elif_ports > 0 and number_of_if_ports != 1:
        raise ValueError(f"Class {ports_class} containing on_elif ports must have exactly one on_if condition")

    if number_of_else_ports > 1:
        raise ValueError(f"Class {ports_class} must have at most one on_else port condition")

    enforce_single_invoked_conditional_port = number_of_elif_ports > 0 or number_of_if_ports <= 1
    return enforce_single_invoked_conditional_port
