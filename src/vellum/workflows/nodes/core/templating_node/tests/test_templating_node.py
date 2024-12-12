import json

from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.nodes.core.templating_node.node import TemplatingNode


def test_templating_node__dict_output():
    # GIVEN a templating node with a dict input that just returns it
    class TemplateNode(TemplatingNode):
        template = "{{ data }}"
        inputs = {
            "data": {
                "key": "value",
            }
        }

    # WHEN the node is run
    node = TemplateNode()
    outputs = node.run()

    # THEN the output is json serializable
    assert json.loads(outputs.result) == {"key": "value"}


def test_templating_node__execution_count_reference():
    # GIVEN a random node
    class OtherNode(BaseNode):
        pass

    # AND a templating node that references the execution count of the random node
    class TemplateNode(TemplatingNode):
        template = "{{ total }}"
        inputs = {
            "total": OtherNode.Execution.count,
        }

    # WHEN the node is run
    node = TemplateNode()
    outputs = node.run()

    # THEN the output is just the total
    assert outputs.result == "0"
