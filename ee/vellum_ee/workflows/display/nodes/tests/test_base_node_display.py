import pytest
from uuid import UUID

from vellum.workflows.nodes.bases import BaseNode
from vellum_ee.workflows.display.nodes.base_node_display import BaseNodeDisplay


@pytest.fixture
def node_with_implicit_properties():
    class MyNode(BaseNode):
        pass

    class MyNodeDisplay(BaseNodeDisplay[MyNode]):
        pass

    expected_id = UUID("ace7f746-4fe6-45c7-8207-fc8a4d0c7f6f")

    return MyNodeDisplay, expected_id


@pytest.fixture
def node_with_explicit_properties():
    explicit_id = UUID("a422f67a-1d37-43f0-bdfc-1e4618c9496d")

    class MyNode(BaseNode):
        pass

    class MyNodeDisplay(BaseNodeDisplay[MyNode]):
        node_id = explicit_id

    return MyNodeDisplay, explicit_id


@pytest.fixture(
    params=[
        "node_with_implicit_properties",
        "node_with_explicit_properties",
    ]
)
def node_info(request):
    return request.getfixturevalue(request.param)


def test_get_id(node_info):
    node_display, expected_id = node_info

    assert node_display().node_id == expected_id
    assert node_display.infer_node_class().__id__ == expected_id
