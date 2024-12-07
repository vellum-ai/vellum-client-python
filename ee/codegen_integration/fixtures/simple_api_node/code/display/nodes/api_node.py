from uuid import UUID

from vellum_ee.workflows.display.nodes import BaseAPINodeDisplay
from vellum_ee.workflows.display.nodes.types import PortDisplayOverrides
from vellum_ee.workflows.display.vellum import NodeDisplayData, NodeDisplayPosition

from ...nodes.api_node import ApiNode


class ApiNodeDisplay(BaseAPINodeDisplay[ApiNode]):
    url_input_id = UUID("d2f4547b-eaa3-4b9a-a0f7-0da0975d4e11")
    method_input_id = UUID("4bc3ec8f-f889-45c2-bad0-5498f28cc8af")
    body_input_id = UUID("65dbcf74-183a-49e0-b553-2a3d25ad741d")
    authorization_type_input_id = UUID("c9b08ce9-2dfc-4cbe-9e65-0bf6f8e248c0")
    bearer_token_value_input_id = UUID("6d330109-ec8e-4c39-af30-63d77f07c35d")
    api_key_header_key_input_id = UUID("908e1fb5-bcba-4388-ae1d-a53d256eda97")
    api_key_header_value_input_id = UUID("efefc4f7-6c95-4561-b7a0-b48533e0c68f")
    text_output_id = UUID("6a3c1704-7020-411d-a440-84b2a481691e")
    json_output_id = UUID("f6f469ae-3f50-4276-a294-43d8d0fcf477")
    status_code_output_id = UUID("6ab9d555-7007-43e1-9f90-d2ca21ea99cf")
    additional_header_key_input_ids = {
        "additional_header_value": UUID("a7a796b5-ac5b-471d-af20-b45c66b699ce"),
        "additional_header_value": UUID("58099189-1676-4d89-a01d-9c1d79ba833a"),
    }
    additional_header_value_input_ids = {
        "additional_header_value": UUID("a7a796b5-ac5b-471d-af20-b45c66b699ce"),
        "additional_header_value": UUID("58099189-1676-4d89-a01d-9c1d79ba833a"),
    }
    node_input_ids_by_name = {
        "method": UUID("4bc3ec8f-f889-45c2-bad0-5498f28cc8af"),
        "url": UUID("d2f4547b-eaa3-4b9a-a0f7-0da0975d4e11"),
        "body": UUID("65dbcf74-183a-49e0-b553-2a3d25ad741d"),
        "authorization_type": UUID("c9b08ce9-2dfc-4cbe-9e65-0bf6f8e248c0"),
        "bearer_token_value": UUID("6d330109-ec8e-4c39-af30-63d77f07c35d"),
        "api_key_header_key": UUID("908e1fb5-bcba-4388-ae1d-a53d256eda97"),
        "api_key_header_value": UUID("efefc4f7-6c95-4561-b7a0-b48533e0c68f"),
        "additional_header_key": UUID("4e7557f4-16ec-4fec-97a6-fe221eae1ee5"),
        "additional_header_value": UUID("58099189-1676-4d89-a01d-9c1d79ba833a"),
    }
    output_display = {}
    port_displays = {ApiNode.Ports.default: PortDisplayOverrides(id=UUID("b8ad3fd2-c96c-4ae8-8eae-d234fb13a139"))}
    display_data = NodeDisplayData(
        position=NodeDisplayPosition(x=1889.865705614568, y=236.61265174506826), width=467, height=288
    )