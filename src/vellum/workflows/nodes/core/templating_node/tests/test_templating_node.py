import json

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
