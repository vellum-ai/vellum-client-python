from uuid import UUID

from vellum_ee.workflows.display.nodes import BaseConditionalNodeDisplay
from vellum_ee.workflows.display.nodes.vellum.conditional_node import RuleIdMap
from vellum_ee.workflows.display.vellum import NodeDisplayData, NodeDisplayPosition

from ...nodes.conditional_node import ConditionalNode


class ConditionalNodeDisplay(BaseConditionalNodeDisplay[ConditionalNode]):
    source_handle_ids = {
        0: UUID("8e2b2af3-db06-4025-9395-a6d08a8b9256"),
        1: UUID("babf673e-0bec-421e-aede-3ea323853bd8"),
        2: UUID("25d955d1-5c7e-4e37-8afe-1015b496e59d"),
    }
    rule_ids = [
        RuleIdMap(
            id=UUID("4011aadf-85fa-41d5-b137-f4c53dd60e84"),
            lhs=RuleIdMap(id=UUID("6a73037b-bd3e-4f09-8bdb-adc6c5834a65"), lhs=None, rhs=None),
            rhs=None,
        ),
        RuleIdMap(
            id=UUID("b695d023-629a-48e1-8ca3-ee6bb9ba40ff"),
            lhs=RuleIdMap(id=UUID("8cb78e86-89d2-4ec6-9537-1fb89dc948d2"), lhs=None, rhs=None),
            rhs=None,
        ),
    ]
    condition_ids = {
        0: UUID("9ade47fe-306e-4815-835f-7815a3f5d488"),
        1: UUID("f1572ff3-df6e-4d87-9149-2323efe2e840"),
        2: UUID("27339e00-c535-436e-95f4-3c70d8bf5762"),
    }
    node_input_ids_by_name = {
        "6a73037b-bd3e-4f09-8bdb-adc6c5834a65.field": UUID("4e5d07ad-0c7d-4149-8cf6-c46a9adf82a5"),
        "6a73037b-bd3e-4f09-8bdb-adc6c5834a65.value": UUID("627bf471-2ddf-48f9-9f49-9eb0a2a242b9"),
        "8cb78e86-89d2-4ec6-9537-1fb89dc948d2.field": UUID("1de0d3fd-2a4c-42eb-918b-f5fbfb1e27b4"),
        "8cb78e86-89d2-4ec6-9537-1fb89dc948d2.value": UUID("b608c4fc-2c4e-4bbb-94d7-12cfa105bbdf"),
    }
    display_data = NodeDisplayData(
        position=NodeDisplayPosition(x=1943.4147273142412, y=292.2355134030261), width=480, height=234
    )
