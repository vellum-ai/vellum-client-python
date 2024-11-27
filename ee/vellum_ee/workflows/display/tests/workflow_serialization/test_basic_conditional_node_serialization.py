import pytest
from unittest import mock

from deepdiff import DeepDiff

from vellum.workflows.expressions.begins_with import BeginsWithExpression
from vellum.workflows.expressions.between import BetweenExpression
from vellum.workflows.expressions.contains import ContainsExpression
from vellum.workflows.expressions.does_not_begin_with import DoesNotBeginWithExpression
from vellum.workflows.expressions.does_not_contain import DoesNotContainExpression
from vellum.workflows.expressions.does_not_end_with import DoesNotEndWithExpression
from vellum.workflows.expressions.does_not_equal import DoesNotEqualExpression
from vellum.workflows.expressions.ends_with import EndsWithExpression
from vellum.workflows.expressions.equals import EqualsExpression
from vellum.workflows.expressions.greater_than import GreaterThanExpression
from vellum.workflows.expressions.greater_than_or_equal_to import GreaterThanOrEqualToExpression
from vellum.workflows.expressions.in_ import InExpression
from vellum.workflows.expressions.is_not_null import IsNotNullExpression
from vellum.workflows.expressions.is_null import IsNullExpression
from vellum.workflows.expressions.less_than import LessThanExpression
from vellum.workflows.expressions.less_than_or_equal_to import LessThanOrEqualToExpression
from vellum.workflows.expressions.not_between import NotBetweenExpression
from vellum.workflows.expressions.not_in import NotInExpression
from vellum_ee.workflows.display.nodes.base_node_vellum_display import BaseNodeVellumDisplay
from vellum_ee.workflows.display.workflows import VellumWorkflowDisplay
from vellum_ee.workflows.display.workflows.get_vellum_workflow_display_class import get_workflow_display

from tests.workflows.basic_conditional_node.workflow import CategoryWorkflow
from tests.workflows.basic_conditional_node.workflow_with_only_one_conditional_node import create_simple_workflow


def test_serialize_workflow():
    # GIVEN a Workflow that uses a ConditionalNode
    # WHEN we serialize it
    workflow_display = get_workflow_display(
        base_display_class=VellumWorkflowDisplay, workflow_class=CategoryWorkflow
    )

    # TODO: Support serialization of BaseNode
    # https://app.shortcut.com/vellum/story/4871/support-serialization-of-base-node
    with mock.patch.object(BaseNodeVellumDisplay, "serialize") as mocked_serialize:
        mocked_serialize.return_value = {"type": "MOCKED"}
        serialized_workflow: dict = workflow_display.serialize()

    # THEN we should get a serialized representation of the Workflow
    assert serialized_workflow.keys() == {
        "workflow_raw_data",
        "input_variables",
        "output_variables",
    }

    # AND its input variables should be what we expect
    input_variables = serialized_workflow["input_variables"]
    assert len(input_variables) == 1
    assert not DeepDiff(
        [
            {
                "id": "eece050a-432e-4a2c-8c87-9480397e4cbf",
                "key": "category",
                "type": "STRING",
                "required": True,
                "default": None,
                "extensions": { "color": None },
            },
        ],
        input_variables,
        ignore_order=True,
    )

    # AND its output variables should be what we expect
    output_variables = serialized_workflow["output_variables"]
    assert len(output_variables) == 5
    assert not DeepDiff(
        [
            {
                "id": "c05f7d96-59a0-4d58-93d7-d451afd3f630",
                "key": "question",
                "type": "STRING",
            },
            {
                "id": "93f2cb75-6fa2-4e46-9488-c0bcd29153c0",
                "key": "compliment",
                "type": "STRING",
            },
            {
                "id": "f936ae31-ba15-4864-8961-86231022a4d7",
                "key": "complaint",
                "type": "STRING",
            },
            {
                "id": "cdbe2adf-9951-409a-b9a8-b8b349037f4f",
                "key": "statement",
                "type": "STRING",
            },
            {
                "id": "62ad462f-f819-4940-99ab-b3f145507f57",
                "key": "fallthrough",
                "type": "STRING",
            },
        ],
        output_variables,
        ignore_order=True,
    )

    # AND its raw data should be what we expect
    workflow_raw_data = serialized_workflow["workflow_raw_data"]
    assert workflow_raw_data.keys() == {"edges", "nodes", "display_data", "definition"}
    assert len(workflow_raw_data["edges"]) == 11
    assert len(workflow_raw_data["nodes"]) == 12

    # AND each node should be serialized correctly
    entrypoint_node = workflow_raw_data["nodes"][0]
    assert entrypoint_node == {
        "id": "089b3201-537a-4ed7-8d15-2524a00e8534",
        "type": "ENTRYPOINT",
        "definition": {
            "bases": [],
            "module": [
                "vellum",
                "workflows",
                "nodes",
                "bases",
                "base",
            ],
            "name": "BaseNode",
        },
        "inputs": [],
        "data": {
            "label": "Entrypoint Node",
            "source_handle_id": "c2f0871d-0d9d-417f-8b0e-c813ccf880ac",
        },
        "display_data": {
            "position": {"x": 0.0, "y": 0.0},
        },
    }

    conditional_node = workflow_raw_data["nodes"][1]
    assert not DeepDiff(
        {
            "id": "9b619e4d-b0a7-4121-9060-100d457868cb",
            "type": "CONDITIONAL",
            "inputs": [
                {
                    "id": "c000588f-a1ca-45aa-b4e2-d54a9786429b",
                    "key": "ebb31657-c763-4e83-bdc6-aa6d1a3116c0.field",
                    "value": {
                        "rules": [
                            {
                                "type": "INPUT_VARIABLE",
                                "data": {
                                    "input_variable_id": "eece050a-432e-4a2c-8c87-9480397e4cbf"
                                },
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "82538f2c-ad80-4bd1-8976-f0f634b3933e",
                    "key": "ebb31657-c763-4e83-bdc6-aa6d1a3116c0.value",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "question"},
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "3fa9312b-a232-4ed7-9c76-45631389b761",
                    "key": "1d7798aa-a6b1-4fe7-842d-4b9a61ba34ab.field",
                    "value": {
                        "rules": [
                            {
                                "type": "INPUT_VARIABLE",
                                "data": {
                                    "input_variable_id": "eece050a-432e-4a2c-8c87-9480397e4cbf"
                                },
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "a0509db6-103c-4049-a3b3-c5ad0eff222e",
                    "key": "1d7798aa-a6b1-4fe7-842d-4b9a61ba34ab.value",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "complaint"},
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "1b38a4f8-023c-41e2-acad-4120589b1589",
                    "key": "76c29692-ab96-45eb-b013-b904d06b675d.field",
                    "value": {
                        "rules": [
                            {
                                "type": "INPUT_VARIABLE",
                                "data": {
                                    "input_variable_id": "eece050a-432e-4a2c-8c87-9480397e4cbf"
                                },
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "6be7cfea-cf7a-4e22-a1c4-b19f89d54b30",
                    "key": "76c29692-ab96-45eb-b013-b904d06b675d.value",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "compliment"},
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "86231451-b6dc-49f6-843b-0c00f84aff47",
                    "key": "beac61ea-68f1-406e-a48b-8f8a0ca5a53b.field",
                    "value": {
                        "rules": [
                            {
                                "type": "INPUT_VARIABLE",
                                "data": {
                                    "input_variable_id": "eece050a-432e-4a2c-8c87-9480397e4cbf"
                                },
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "96c8658f-c7db-41f8-be1f-d62350adb149",
                    "key": "beac61ea-68f1-406e-a48b-8f8a0ca5a53b.value",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "statement"},
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "86231451-b6dc-49f6-843b-0c00f84aff47",
                    "key": "beac61ea-68f1-406e-a48b-8f8a0ca5a53b.field",
                    "value": {
                        "rules": [
                            {
                                "type": "INPUT_VARIABLE",
                                "data": {
                                    "input_variable_id": "eece050a-432e-4a2c-8c87-9480397e4cbf"
                                },
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "96c8658f-c7db-41f8-be1f-d62350adb149",
                    "key": "beac61ea-68f1-406e-a48b-8f8a0ca5a53b.value",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "statement"},
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "86231451-b6dc-49f6-843b-0c00f84aff47",
                    "key": "beac61ea-68f1-406e-a48b-8f8a0ca5a53b.field",
                    "value": {
                        "rules": [
                            {
                                "type": "INPUT_VARIABLE",
                                "data": {
                                    "input_variable_id": "eece050a-432e-4a2c-8c87-9480397e4cbf"
                                },
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "96c8658f-c7db-41f8-be1f-d62350adb149",
                    "key": "beac61ea-68f1-406e-a48b-8f8a0ca5a53b.value",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "statement"},
                            }
                        ],
                        "combinator": "OR",
                    },
                },
            ],
            "data": {
                "label": "Category Conditional Node",
                "target_handle_id": "dd89e228-a23e-422b-80b2-34362c1c050e",
                "conditions": [
                    {
                        "id": "de7b0b4e-7803-4d36-a275-2e7e3f60342b",
                        "type": "IF",
                        "source_handle_id": "561b4e3a-8db3-448a-8933-1115937082ff",
                        "data": {
                            "id": "2ccd0730-26d1-4fb4-baa9-1a2a182dd9a0",
                            "rules": [
                                {
                                    "id": "ebb31657-c763-4e83-bdc6-aa6d1a3116c0",
                                    "rules": None,
                                    "combinator": None,
                                    "negated": False,
                                    "field_node_input_id": "c000588f-a1ca-45aa-b4e2-d54a9786429b",
                                    "operator": "=",
                                    "value_node_input_id": "82538f2c-ad80-4bd1-8976-f0f634b3933e",
                                }
                            ],
                            "combinator": "AND",
                            "negated": False,
                            "field_node_input_id": None,
                            "operator": None,
                            "value_node_input_id": None,
                        },
                    },
                    {
                        "id": "5e783d17-6808-441a-ac6c-33a4e184f4e0",
                        "type": "ELIF",
                        "source_handle_id": "0644f22e-2680-441a-9554-eedf1d3d22a9",
                        "data": {
                            "id": "cc3f0d92-b603-42cc-b2e9-83e3b23b3bcb",
                            "rules": [
                                {
                                    "id": "1d7798aa-a6b1-4fe7-842d-4b9a61ba34ab",
                                    "rules": None,
                                    "combinator": None,
                                    "negated": False,
                                    "field_node_input_id": "3fa9312b-a232-4ed7-9c76-45631389b761",
                                    "operator": "=",
                                    "value_node_input_id": "a0509db6-103c-4049-a3b3-c5ad0eff222e",
                                }
                            ],
                            "combinator": "AND",
                            "negated": False,
                            "field_node_input_id": None,
                            "operator": None,
                            "value_node_input_id": None,
                        },
                    },
                    {
                        "id": "6bd2f643-9cf5-4e7f-9113-f90e5c8057be",
                        "type": "ELIF",
                        "source_handle_id": "2a48d274-ecfc-4f40-95ac-bc697663f10c",
                        "data": {
                            "id": "a5a0f391-7052-452f-9fe1-a5781a491591",
                            "rules": [
                                {
                                    "id": "76c29692-ab96-45eb-b013-b904d06b675d",
                                    "rules": None,
                                    "combinator": None,
                                    "negated": False,
                                    "field_node_input_id": "1b38a4f8-023c-41e2-acad-4120589b1589",
                                    "operator": "=",
                                    "value_node_input_id": "6be7cfea-cf7a-4e22-a1c4-b19f89d54b30",
                                }
                            ],
                            "combinator": "AND",
                            "negated": False,
                            "field_node_input_id": None,
                            "operator": None,
                            "value_node_input_id": None,
                        },
                    },
                    {
                        "id": "0a058485-18a4-4e20-8a30-6da8196ac46f",
                        "type": "ELIF",
                        "source_handle_id": "90fc9dc8-0a74-4a98-b6ac-55ffce4a2881",
                        "data": {
                            "id": "efe7a851-2a67-4189-99ec-bc193242b270",
                            "rules": [
                                {
                                    "id": "beac61ea-68f1-406e-a48b-8f8a0ca5a53b",
                                    "rules": None,
                                    "combinator": None,
                                    "negated": False,
                                    "field_node_input_id": "86231451-b6dc-49f6-843b-0c00f84aff47",
                                    "operator": "=",
                                    "value_node_input_id": "96c8658f-c7db-41f8-be1f-d62350adb149",
                                },
                                {
                                    "id": "2c78817b-8b73-43fd-8dab-a8923018da9d",
                                    "rules": [
                                        {
                                            "id": "beac61ea-68f1-406e-a48b-8f8a0ca5a53b",
                                            "rules": None,
                                            "combinator": None,
                                            "negated": False,
                                            "field_node_input_id": "86231451-b6dc-49f6-843b-0c00f84aff47",
                                            "operator": "=",
                                            "value_node_input_id": "96c8658f-c7db-41f8-be1f-d62350adb149",
                                        },
                                        {
                                            "id": "beac61ea-68f1-406e-a48b-8f8a0ca5a53b",
                                            "rules": None,
                                            "combinator": None,
                                            "negated": False,
                                            "field_node_input_id": "86231451-b6dc-49f6-843b-0c00f84aff47",
                                            "operator": "=",
                                            "value_node_input_id": "96c8658f-c7db-41f8-be1f-d62350adb149",
                                        },
                                    ],
                                    "combinator": "AND",
                                    "negated": False,
                                    "field_node_input_id": None,
                                    "operator": None,
                                    "value_node_input_id": None,
                                },
                            ],
                            "combinator": "AND",
                            "negated": False,
                            "field_node_input_id": None,
                            "operator": None,
                            "value_node_input_id": None,
                        },
                    },
                    {
                        "id": "c2fa8a44-923b-462a-b0d2-fa800a152e52",
                        "type": "ELSE",
                        "source_handle_id": "493024f4-8010-4e1a-abae-b6adbc6fb208",
                        "data": None,
                    },
                ],
                "version": "2",
            },
            "display_data": {"position": {"x": 0.0, "y": 0.0}},
            "definition": {
                "name": "CategoryConditionalNode",
                "module": ["tests", "workflows", "basic_conditional_node", "workflow"],
                "bases": [
                    {
                        "name": "ConditionalNode",
                        "module": [
                            "vellum",
                            "workflows",
                            "nodes",
                            "displayable",
                            "conditional_node",
                            "node",
                        ],
                    }
                ],
            },
        },
        conditional_node,
        ignore_order=True,
    )

    assert not DeepDiff(
        [
            {
                "type": "MOCKED",
            },
            {
                "type": "MOCKED",
            },
            {
                "type": "MOCKED",
            },
            {
                "type": "MOCKED",
            },
            {
                "type": "MOCKED",
            },
        ],
        workflow_raw_data["nodes"][2:7],
    )

    assert not DeepDiff(
        [
            {
                "id": "9c22ee47-01da-4e4e-863d-b4a6874bed66",
                "type": "TERMINAL",
                "definition": {
                    "bases": [
                        {
                            "bases": [],
                            "module": [
                                "vellum",
                                "workflows",
                                "nodes",
                                "bases",
                                "base",
                            ],
                            "name": "BaseNode",
                        },
                    ],
                    "module": [
                        "vellum",
                        "workflows",
                        "nodes",
                        "displayable",
                        "final_output_node",
                        "node",
                    ],
                    "name": "FinalOutputNode",
                },
                "data": {
                    "label": "Final Output",
                    "name": "statement",
                    "target_handle_id": "f02a8971-e9a4-4716-bfb4-d08f5614b5d8",
                    "output_id": "cdbe2adf-9951-409a-b9a8-b8b349037f4f",
                    "output_type": "STRING",
                    "node_input_id": "bed69f8a-3a83-4e52-beba-8eb14f4b0ca9",
                },
                "inputs": [
                    {
                        "id": "bed69f8a-3a83-4e52-beba-8eb14f4b0ca9",
                        "key": "node_input",
                        "value": {
                            "rules": [
                                {
                                    "type": "NODE_OUTPUT",
                                    "data": {
                                        "node_id": "ed7caf01-9ae7-47a3-b15a-16697abaf486",
                                        "output_id": "74ea6af1-8934-4e3c-b68d-b93092b4be73",
                                    },
                                }
                            ],
                            "combinator": "OR",
                        },
                    }
                ],
                "display_data": {"position": {"x": 0.0, "y": 0.0}},
            },
            {
                "id": "47f0931c-41f6-4b84-bf39-0c486941f599",
                "type": "TERMINAL",
                "definition": {
                    "bases": [
                        {
                            "bases": [],
                            "module": [
                                "vellum",
                                "workflows",
                                "nodes",
                                "bases",
                                "base",
                            ],
                            "name": "BaseNode",
                        },
                    ],
                    "module": [
                        "vellum",
                        "workflows",
                        "nodes",
                        "displayable",
                        "final_output_node",
                        "node",
                    ],
                    "name": "FinalOutputNode",
                },
                "data": {
                    "label": "Final Output",
                    "name": "compliment",
                    "target_handle_id": "a4d57adc-58c1-40c6-810b-ee5fd923bfc5",
                    "output_id": "93f2cb75-6fa2-4e46-9488-c0bcd29153c0",
                    "output_type": "STRING",
                    "node_input_id": "e3f2d793-31a7-4670-8155-bd034d9f25e2",
                },
                "inputs": [
                    {
                        "id": "e3f2d793-31a7-4670-8155-bd034d9f25e2",
                        "key": "node_input",
                        "value": {
                            "rules": [
                                {
                                    "type": "NODE_OUTPUT",
                                    "data": {
                                        "node_id": "8df781b1-ff28-48a5-98a2-d7d796b932b0",
                                        "output_id": "61c357a1-41d8-4adf-bfe1-ce615c4d7d23",
                                    },
                                }
                            ],
                            "combinator": "OR",
                        },
                    }
                ],
                "display_data": {"position": {"x": 0.0, "y": 0.0}},
            },
            {
                "id": "e3d29229-f746-4125-819e-f847acbed307",
                "type": "TERMINAL",
                "definition": {
                    "bases": [
                        {
                            "bases": [],
                            "module": [
                                "vellum",
                                "workflows",
                                "nodes",
                                "bases",
                                "base",
                            ],
                            "name": "BaseNode",
                        },
                    ],
                    "module": [
                        "vellum",
                        "workflows",
                        "nodes",
                        "displayable",
                        "final_output_node",
                        "node",
                    ],
                    "name": "FinalOutputNode",
                },
                "data": {
                    "label": "Final Output",
                    "name": "complaint",
                    "target_handle_id": "c5dd9bf5-9e18-4dbc-8c20-2c0baf969ebe",
                    "output_id": "f936ae31-ba15-4864-8961-86231022a4d7",
                    "output_type": "STRING",
                    "node_input_id": "9b35cc61-5887-478a-814d-9693ead5932f",
                },
                "inputs": [
                    {
                        "id": "9b35cc61-5887-478a-814d-9693ead5932f",
                        "key": "node_input",
                        "value": {
                            "rules": [
                                {
                                    "type": "NODE_OUTPUT",
                                    "data": {
                                        "node_id": "68c02b7c-5077-4087-803d-841474a8081f",
                                        "output_id": "0ec68ffe-cbb7-4dbb-aaff-f6025bd62efa",
                                    },
                                }
                            ],
                            "combinator": "OR",
                        },
                    }
                ],
                "display_data": {"position": {"x": 0.0, "y": 0.0}},
            },
            {
                "id": "6efa7b45-0580-406d-85aa-439117ba8021",
                "type": "TERMINAL",
                "definition": {
                    "bases": [
                        {
                            "bases": [],
                            "module": [
                                "vellum",
                                "workflows",
                                "nodes",
                                "bases",
                                "base",
                            ],
                            "name": "BaseNode",
                        },
                    ],
                    "module": [
                        "vellum",
                        "workflows",
                        "nodes",
                        "displayable",
                        "final_output_node",
                        "node",
                    ],
                    "name": "FinalOutputNode",
                },
                "data": {
                    "label": "Final Output",
                    "name": "fallthrough",
                    "target_handle_id": "2283cd2c-b077-4b5d-a96f-aa2cd6023eda",
                    "output_id": "62ad462f-f819-4940-99ab-b3f145507f57",
                    "output_type": "STRING",
                    "node_input_id": "cee5378a-9011-4d03-bd3c-a32421bd093f",
                },
                "inputs": [
                    {
                        "id": "cee5378a-9011-4d03-bd3c-a32421bd093f",
                        "key": "node_input",
                        "value": {
                            "rules": [
                                {
                                    "type": "NODE_OUTPUT",
                                    "data": {
                                        "node_id": "148c61bd-e8b0-4d4b-8734-b043a72b90ed",
                                        "output_id": "fafa0bde-8508-43d5-a9c8-db5d49f307f6",
                                    },
                                }
                            ],
                            "combinator": "OR",
                        },
                    }
                ],
                "display_data": {"position": {"x": 0.0, "y": 0.0}},
            },
            {
                "id": "fa11b84b-1d76-4adc-ab28-cbbaa933c267",
                "type": "TERMINAL",
                "definition": {
                    "bases": [
                        {
                            "bases": [],
                            "module": [
                                "vellum",
                                "workflows",
                                "nodes",
                                "bases",
                                "base",
                            ],
                            "name": "BaseNode",
                        },
                    ],
                    "module": [
                        "vellum",
                        "workflows",
                        "nodes",
                        "displayable",
                        "final_output_node",
                        "node",
                    ],
                    "name": "FinalOutputNode",
                },
                "data": {
                    "label": "Final Output",
                    "name": "question",
                    "target_handle_id": "e1a6da28-02c5-40d7-8ac5-9fb07e2e3e1d",
                    "output_id": "c05f7d96-59a0-4d58-93d7-d451afd3f630",
                    "output_type": "STRING",
                    "node_input_id": "1c1d34d9-0cda-471f-ac9a-40ac351c9aca",
                },
                "inputs": [
                    {
                        "id": "1c1d34d9-0cda-471f-ac9a-40ac351c9aca",
                        "key": "node_input",
                        "value": {
                            "rules": [
                                {
                                    "type": "NODE_OUTPUT",
                                    "data": {
                                        "node_id": "0d959311-c836-4641-a867-58f63df9dfea",
                                        "output_id": "db9f7ff3-77e2-4b0a-9c39-bb4bb50e3ad5",
                                    },
                                }
                            ],
                            "combinator": "OR",
                        },
                    }
                ],
                "display_data": {"position": {"x": 0.0, "y": 0.0}},
            },
        ],
        workflow_raw_data["nodes"][7:12],
        ignore_order=True,
    )

    # AND each edge should be serialized correctly
    serialized_edges = workflow_raw_data["edges"]
    assert not DeepDiff(
        [
            {
                "id": "32263c88-d725-4d03-a500-fadc34e10c9a",
                "source_node_id": "089b3201-537a-4ed7-8d15-2524a00e8534",
                "source_handle_id": "c2f0871d-0d9d-417f-8b0e-c813ccf880ac",
                "target_node_id": "9b619e4d-b0a7-4121-9060-100d457868cb",
                "target_handle_id": "dd89e228-a23e-422b-80b2-34362c1c050e",
                "type": "DEFAULT",
            },
            {
                "id": "1ae3cdb6-5b52-4ad3-bcfe-6997c86083f8",
                "source_node_id": "9b619e4d-b0a7-4121-9060-100d457868cb",
                "source_handle_id": "3a45b81f-95e4-4cbd-8997-bfdbe30251e8",
                "target_node_id": "0d959311-c836-4641-a867-58f63df9dfea",
                "target_handle_id": "7beba198-c452-4749-a38a-ea9420d84e14",
                "type": "DEFAULT",
            },
            {
                "id": "5704cb9c-9d01-4809-9d91-8014276e6574",
                "source_node_id": "9b619e4d-b0a7-4121-9060-100d457868cb",
                "source_handle_id": "7202f702-1ebc-4067-ab1e-ec67e49158ee",
                "target_node_id": "68c02b7c-5077-4087-803d-841474a8081f",
                "target_handle_id": "1dc4eebe-b6db-4229-96e5-115ff8cedb76",
                "type": "DEFAULT",
            },
            {
                "id": "c923e009-06c9-4978-b789-6ae995dcc81c",
                "source_node_id": "9b619e4d-b0a7-4121-9060-100d457868cb",
                "source_handle_id": "cf45705d-1a47-43a6-9d24-a7fdf78baae0",
                "target_node_id": "8df781b1-ff28-48a5-98a2-d7d796b932b0",
                "target_handle_id": "b73c39be-cbfe-4225-86e6-e6e4c161881e",
                "type": "DEFAULT",
            },
            {
                "id": "e487c031-fd5b-41b3-94d7-eb3f7ce8e25c",
                "source_node_id": "9b619e4d-b0a7-4121-9060-100d457868cb",
                "source_handle_id": "f04610dd-61cf-41b0-b337-2235e101cdb0",
                "target_node_id": "ed7caf01-9ae7-47a3-b15a-16697abaf486",
                "target_handle_id": "76fe7aec-5cd4-4c1a-b386-cfe09ebe66e4",
                "type": "DEFAULT",
            },
            {
                "id": "6a1c379d-bbe4-4034-8ac9-0353901ebc21",
                "source_node_id": "9b619e4d-b0a7-4121-9060-100d457868cb",
                "source_handle_id": "f9dde637-ea90-465f-a871-caf8380ae377",
                "target_node_id": "148c61bd-e8b0-4d4b-8734-b043a72b90ed",
                "target_handle_id": "c88839af-3a79-4310-abbd-e1553d981dce",
                "type": "DEFAULT",
            },
            {
                "id": "8a554637-e382-4a66-9b77-4eadce45a25a",
                "source_node_id": "ed7caf01-9ae7-47a3-b15a-16697abaf486",
                "source_handle_id": "cde43aef-f607-4b5d-87f6-9238dd4a3a2b",
                "target_node_id": "9c22ee47-01da-4e4e-863d-b4a6874bed66",
                "target_handle_id": "f02a8971-e9a4-4716-bfb4-d08f5614b5d8",
                "type": "DEFAULT",
            },
            {
                "id": "af083f7d-226c-4341-bb6f-756f00846b42",
                "source_node_id": "68c02b7c-5077-4087-803d-841474a8081f",
                "source_handle_id": "ef032cf7-c8df-4a98-827c-386dd8a5a346",
                "target_node_id": "e3d29229-f746-4125-819e-f847acbed307",
                "target_handle_id": "c5dd9bf5-9e18-4dbc-8c20-2c0baf969ebe",
                "type": "DEFAULT",
            },
            {
                "id": "47758209-70cb-4f12-b71f-dc28df0f6d0b",
                "source_node_id": "0d959311-c836-4641-a867-58f63df9dfea",
                "source_handle_id": "69a2121d-fc21-47a1-af49-6200aad836de",
                "target_node_id": "fa11b84b-1d76-4adc-ab28-cbbaa933c267",
                "target_handle_id": "e1a6da28-02c5-40d7-8ac5-9fb07e2e3e1d",
                "type": "DEFAULT",
            },
            {
                "id": "f08a49f8-8bfd-4c05-8f28-dfa536654af8",
                "source_node_id": "8df781b1-ff28-48a5-98a2-d7d796b932b0",
                "source_handle_id": "aeb6805d-2c9f-4d52-a690-341ea0e869b3",
                "target_node_id": "47f0931c-41f6-4b84-bf39-0c486941f599",
                "target_handle_id": "a4d57adc-58c1-40c6-810b-ee5fd923bfc5",
                "type": "DEFAULT",
            },
            {
                "id": "c45e03b4-dba6-4620-bc02-3847ad90086b",
                "source_node_id": "148c61bd-e8b0-4d4b-8734-b043a72b90ed",
                "source_handle_id": "26f50353-85ae-462f-b82d-9fd736900bd6",
                "target_node_id": "6efa7b45-0580-406d-85aa-439117ba8021",
                "target_handle_id": "2283cd2c-b077-4b5d-a96f-aa2cd6023eda",
                "type": "DEFAULT",
            },
        ],
        serialized_edges,
        ignore_order=True,
    )

    # AND the display data should be what we expect
    display_data = workflow_raw_data["display_data"]
    assert display_data == {
        "viewport": {
            "x": 0.0,
            "y": 0.0,
            "zoom": 1.0,
        }
    }

    # AND the definition should be what we expect
    definition = workflow_raw_data["definition"]
    assert definition == {
        "name": "CategoryWorkflow",
        "module": [
            "tests",
            "workflows",
            "basic_conditional_node",
            "workflow",
        ],
    }


def descriptors_with_lhs_and_rhs():
    return [
        (EqualsExpression(lhs="123", rhs="123"), "="),
        (DoesNotEqualExpression(lhs="123", rhs="123"), "!="),
        (LessThanExpression(lhs="123", rhs="123"), "<"),
        (GreaterThanExpression(lhs="123", rhs="123"), ">"),
        (LessThanOrEqualToExpression(lhs="123", rhs="123"), "<="),
        (GreaterThanOrEqualToExpression(lhs="123", rhs="123"), ">="),
        (ContainsExpression(lhs="123", rhs="123"), "contains"),
        (BeginsWithExpression(lhs="123", rhs="123"), "beginsWith"),
        (EndsWithExpression(lhs="123", rhs="123"), "endsWith"),
        (DoesNotContainExpression(lhs="123", rhs="123"), "doesNotContain"),
        (DoesNotBeginWithExpression(lhs="123", rhs="123"), "doesNotBeginWith"),
        (DoesNotEndWithExpression(lhs="123", rhs="123"), "doesNotEndWith"),
        (InExpression(lhs="123", rhs="123"), "in"),
        (NotInExpression(lhs="123", rhs="123"), "notIn"),
    ]


def descriptors_with_expression():
    return [
        (IsNullExpression(expression="123"), "null"),
        (IsNotNullExpression(expression="123"), "notNull"),
    ]


def descriptors_with_value_and_start_and_end():
    return [
        (BetweenExpression(value="123", start="123", end="123"), "between"),
        (NotBetweenExpression(value="123", start="123", end="123"), "notBetween"),
    ]


@pytest.mark.parametrize("descriptor, operator", descriptors_with_lhs_and_rhs())
def test_conditional_node_serialize_all_operators_with_lhs_and_rhs(
    descriptor, operator
):
    # GIVEN a simple workflow with one conditional node
    workflow_cls = create_simple_workflow(descriptor)

    workflow_display = get_workflow_display(
        base_display_class=VellumWorkflowDisplay, workflow_class=workflow_cls
    )

    # TODO: Support serialization of BaseNode
    # https://app.shortcut.com/vellum/story/4871/support-serialization-of-base-node
    with mock.patch.object(BaseNodeVellumDisplay, "serialize") as mocked_serialize:
        mocked_serialize.return_value = {"type": "MOCKED"}
        serialized_workflow: dict = workflow_display.serialize()

    # THEN we should get a serialized representation of the Workflow
    assert serialized_workflow.keys() == {
        "workflow_raw_data",
        "input_variables",
        "output_variables",
    }

    # AND its raw data should be what we expect
    workflow_raw_data = serialized_workflow["workflow_raw_data"]
    assert workflow_raw_data.keys() == {"edges", "nodes", "display_data", "definition"}

    # AND the conditional node should be what we expect
    conditional_node = workflow_raw_data["nodes"][1]
    assert not DeepDiff(
        {
            "id": "a9143814-6bb0-4cb3-a817-4fc076417121",
            "type": "CONDITIONAL",
            "inputs": [
                {
                    "id": "2262b7b4-a2f2-408b-9d4d-362940ca1ed3",
                    "key": "abe7afac-952f-4cfc-ab07-47b47f34105f.field",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "123"},
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "aadade8a-c253-483a-8620-31fe8171c0fd",
                    "key": "abe7afac-952f-4cfc-ab07-47b47f34105f.value",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "123"},
                            }
                        ],
                        "combinator": "OR",
                    },
                },
            ],
            "data": {
                "label": "Simple Conditional Node",
                "target_handle_id": "c6e99e94-bc8e-47a4-b75c-cc96c6bedbb0",
                "conditions": [
                    {
                        "id": "a4c32611-fd58-4b98-9d08-313cfd1c214e",
                        "type": "IF",
                        "source_handle_id": "8124a6cf-4a34-4149-adc0-68696c11bd4e",
                        "data": {
                            "id": "650e7105-3e76-43ca-858f-b290970b438b",
                            "rules": [
                                {
                                    "id": "abe7afac-952f-4cfc-ab07-47b47f34105f",
                                    "rules": None,
                                    "combinator": None,
                                    "negated": False,
                                    "field_node_input_id": "2262b7b4-a2f2-408b-9d4d-362940ca1ed3",
                                    "operator": f"{operator}",
                                    "value_node_input_id": "aadade8a-c253-483a-8620-31fe8171c0fd",
                                }
                            ],
                            "combinator": "AND",
                            "negated": False,
                            "field_node_input_id": None,
                            "operator": None,
                            "value_node_input_id": None,
                        },
                    }
                ],
                "version": "2",
            },
            "display_data": {"position": {"x": 0.0, "y": 0.0}},
            "definition": {
                "bases": [
                    {
                        "module": [
                            "vellum",
                            "workflows",
                            "nodes",
                            "displayable",
                            "conditional_node",
                            "node",
                        ],
                        "name": "ConditionalNode",
                    }
                ],
                "module": [
                    "tests",
                    "workflows",
                    "basic_conditional_node",
                    "workflow_with_only_one_conditional_node",
                ],
                "name": "SimpleConditionalNode",
            },
        },
        conditional_node,
        ignore_order=True,
    )


@pytest.mark.parametrize("descriptor, operator", descriptors_with_expression())
def test_conditional_node_serialize_all_operators_with_expression(descriptor, operator):
    # GIVEN a simple workflow with one conditional node
    workflow_cls = create_simple_workflow(descriptor)

    workflow_display = get_workflow_display(
        base_display_class=VellumWorkflowDisplay, workflow_class=workflow_cls
    )

    # TODO: Support serialization of BaseNode
    # https://app.shortcut.com/vellum/story/4871/support-serialization-of-base-node
    with mock.patch.object(BaseNodeVellumDisplay, "serialize") as mocked_serialize:
        mocked_serialize.return_value = {"type": "MOCKED"}
        serialized_workflow: dict = workflow_display.serialize()

    # THEN we should get a serialized representation of the Workflow
    assert serialized_workflow.keys() == {
        "workflow_raw_data",
        "input_variables",
        "output_variables",
    }

    # AND its raw data should be what we expect
    workflow_raw_data = serialized_workflow["workflow_raw_data"]
    assert workflow_raw_data.keys() == {"edges", "nodes", "display_data", "definition"}

    # AND the conditional node should be what we expect
    conditional_node = workflow_raw_data["nodes"][1]
    assert not DeepDiff(
        {
            "id": "a9143814-6bb0-4cb3-a817-4fc076417121",
            "type": "CONDITIONAL",
            "inputs": [
                {
                    "id": "2262b7b4-a2f2-408b-9d4d-362940ca1ed3",
                    "key": "abe7afac-952f-4cfc-ab07-47b47f34105f.field",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "123"},
                            }
                        ],
                        "combinator": "OR",
                    },
                }
            ],
            "data": {
                "label": "Simple Conditional Node",
                "target_handle_id": "c6e99e94-bc8e-47a4-b75c-cc96c6bedbb0",
                "conditions": [
                    {
                        "id": "a4c32611-fd58-4b98-9d08-313cfd1c214e",
                        "type": "IF",
                        "source_handle_id": "8124a6cf-4a34-4149-adc0-68696c11bd4e",
                        "data": {
                            "id": "650e7105-3e76-43ca-858f-b290970b438b",
                            "rules": [
                                {
                                    "id": "abe7afac-952f-4cfc-ab07-47b47f34105f",
                                    "rules": None,
                                    "combinator": None,
                                    "negated": False,
                                    "field_node_input_id": "2262b7b4-a2f2-408b-9d4d-362940ca1ed3",
                                    "operator": f"{operator}",
                                    "value_node_input_id": None,
                                }
                            ],
                            "combinator": "AND",
                            "negated": False,
                            "field_node_input_id": None,
                            "operator": None,
                            "value_node_input_id": None,
                        },
                    }
                ],
                "version": "2",
            },
            "display_data": {"position": {"x": 0.0, "y": 0.0}},
            "definition": {
                "bases": [
                    {
                        "module": [
                            "vellum",
                            "workflows",
                            "nodes",
                            "displayable",
                            "conditional_node",
                            "node",
                        ],
                        "name": "ConditionalNode",
                    }
                ],
                "module": [
                    "tests",
                    "workflows",
                    "basic_conditional_node",
                    "workflow_with_only_one_conditional_node",
                ],
                "name": "SimpleConditionalNode",
            },
        },
        conditional_node,
        ignore_order=True,
    )


@pytest.mark.parametrize(
    "descriptor, operator", descriptors_with_value_and_start_and_end()
)
def test_conditional_node_serialize_all_operators_with_value_and_start_and_end(
    descriptor, operator
):
    # GIVEN a simple workflow with one conditional node
    workflow_cls = create_simple_workflow(descriptor)

    workflow_display = get_workflow_display(
        base_display_class=VellumWorkflowDisplay, workflow_class=workflow_cls
    )

    # TODO: Support serialization of BaseNode
    # https://app.shortcut.com/vellum/story/4871/support-serialization-of-base-node
    with mock.patch.object(BaseNodeVellumDisplay, "serialize") as mocked_serialize:
        mocked_serialize.return_value = {"type": "MOCKED"}
        serialized_workflow: dict = workflow_display.serialize()

    # THEN we should get a serialized representation of the Workflow
    assert serialized_workflow.keys() == {
        "workflow_raw_data",
        "input_variables",
        "output_variables",
    }

    # AND its raw data should be what we expect
    workflow_raw_data = serialized_workflow["workflow_raw_data"]
    assert workflow_raw_data.keys() == {"edges", "nodes", "display_data", "definition"}

    # AND the conditional node should be what we expect
    conditional_node = workflow_raw_data["nodes"][1]
    assert not DeepDiff(
        {
            "id": "a9143814-6bb0-4cb3-a817-4fc076417121",
            "type": "CONDITIONAL",
            "inputs": [
                {
                    "id": "2262b7b4-a2f2-408b-9d4d-362940ca1ed3",
                    "key": "abe7afac-952f-4cfc-ab07-47b47f34105f.field",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "123"},
                            }
                        ],
                        "combinator": "OR",
                    },
                },
                {
                    "id": "aadade8a-c253-483a-8620-31fe8171c0fd",
                    "key": "abe7afac-952f-4cfc-ab07-47b47f34105f.value",
                    "value": {
                        "rules": [
                            {
                                "type": "CONSTANT_VALUE",
                                "data": {"type": "STRING", "value": "123,123"},
                            }
                        ],
                        "combinator": "OR",
                    },
                },
            ],
            "data": {
                "label": "Simple Conditional Node",
                "target_handle_id": "c6e99e94-bc8e-47a4-b75c-cc96c6bedbb0",
                "conditions": [
                    {
                        "id": "a4c32611-fd58-4b98-9d08-313cfd1c214e",
                        "type": "IF",
                        "source_handle_id": "8124a6cf-4a34-4149-adc0-68696c11bd4e",
                        "data": {
                            "id": "650e7105-3e76-43ca-858f-b290970b438b",
                            "rules": [
                                {
                                    "id": "abe7afac-952f-4cfc-ab07-47b47f34105f",
                                    "rules": None,
                                    "combinator": None,
                                    "negated": False,
                                    "field_node_input_id": "2262b7b4-a2f2-408b-9d4d-362940ca1ed3",
                                    "operator": f"{operator}",
                                    "value_node_input_id": "aadade8a-c253-483a-8620-31fe8171c0fd",
                                }
                            ],
                            "combinator": "AND",
                            "negated": False,
                            "field_node_input_id": None,
                            "operator": None,
                            "value_node_input_id": None,
                        },
                    }
                ],
                "version": "2",
            },
            "display_data": {"position": {"x": 0.0, "y": 0.0}},
            "definition": {
                "bases": [
                    {
                        "module": [
                            "vellum",
                            "workflows",
                            "nodes",
                            "displayable",
                            "conditional_node",
                            "node",
                        ],
                        "name": "ConditionalNode",
                    }
                ],
                "module": [
                    "tests",
                    "workflows",
                    "basic_conditional_node",
                    "workflow_with_only_one_conditional_node",
                ],
                "name": "SimpleConditionalNode",
            },
        },
        conditional_node,
        ignore_order=True,
    )
