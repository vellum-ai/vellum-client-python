from tests.workflows.basic_inline_subworkflow.workflow import BasicInlineSubworkflowWorkflow, Inputs


def test_run_workflow__happy_path():
    # GIVEN a workflow that's set up to hit an inline Subworkflow
    workflow = BasicInlineSubworkflowWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run(
        inputs=Inputs(
            city="San Francisco",
            date="2024-01-01",
        )
    )

    # THEN the workflow should have completed successfully
    assert terminal_event.name == "workflow.execution.fulfilled"

    # AND the outputs should be as expected
    assert terminal_event.outputs == {
        "temperature": 70,
        "reasoning": "The weather in San Francisco on 2024-01-01 was hot",
    }
