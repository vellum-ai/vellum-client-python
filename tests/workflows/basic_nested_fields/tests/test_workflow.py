import os

from tests.workflows.basic_nested_fields.workflow import BasicNestedFieldsWorkflow, ExampleCustomClass, Inputs


def test_run_workflow__happy_path():
    # GIVEN a known environment and workflow
    os.environ["EXAMPLE_ENV_VAR"] = "https://api.vellum.ai"
    workflow = BasicNestedFieldsWorkflow()

    # WHEN I run the workflow
    terminal_event = workflow.run(inputs=Inputs(input_value=3))

    # THEN I should have been able to resolve all of its fields and produce the expected outputs
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs == {
        "simple_field": 3,
        "state_field": 5,
        "nested_array_field": ["a", {"b": 3}, "c"],
        "nested_field": ExampleCustomClass(field=3, nested=ExampleCustomClass(field=3, nested=None)),
        "super_nested_field": 3,
        "nested_dict_field": {"key": 3},
        "node_output_field": 1,
        "env_field": "https://api.vellum.ai",
    }
