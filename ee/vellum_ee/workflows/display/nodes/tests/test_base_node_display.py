import pytest
from uuid import UUID

from vellum_ee.workflows.display.nodes.base_node_display import BaseNodeDisplay
from vellum.workflows.nodes.bases import BaseNode


@pytest.fixture
def node_with_implicit_properties():
    class MyNode(BaseNode):
        pass

    class MyNodeDisplay(BaseNodeDisplay[MyNode]):
        pass

    expected_id = UUID("ace7f746-4fe6-45c7-8207-fc8a4d0c7f6f")

    return MyNode, MyNodeDisplay, expected_id


@pytest.fixture
def node_with_explicit_properties():
    explicit_id = UUID("a422f67a-1d37-43f0-bdfc-1e4618c9496d")

    class MyNode(BaseNode):
        pass

    class MyNodeDisplay(BaseNodeDisplay[MyNode]):
        node_id = explicit_id

    return MyNode, MyNodeDisplay, explicit_id


@pytest.fixture(
    params=[
        "node_with_implicit_properties",
        "node_with_explicit_properties",
    ]
)
def node_info(request):
    return request.getfixturevalue(request.param)


def test_get_id(node_info):
    node, node_display, expected_id = node_info

    assert node_display(node).node_id == expected_id
