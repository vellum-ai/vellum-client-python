from datetime import datetime, timedelta

from tests.workflows.basic_templating_node.workflow import BasicTemplatingNodeWorkflow, Inputs


def test_run_workflow__happy_path():
    """Confirm that we can successfully invoke a Workflow with a single Templating Node"""

    # GIVEN a workflow that's set up run a Templating Node
    workflow = BasicTemplatingNodeWorkflow()

    # WHEN we run the workflow
    terminal_event = workflow.run(
        inputs=Inputs(
            city="San Francisco",
            weather="stormy",
        )
    )

    # THEN the workflow should have completed successfully
    assert terminal_event.name == "workflow.execution.fulfilled"

    # AND the outputs should be as expected
    assert terminal_event.outputs.result.startswith("The weather in San Francisco on ")
    assert terminal_event.outputs.result.endswith(" is stormy.")

    # AND the datetime should be appropriate for the current time
    datetime_str = terminal_event.outputs.result.split("The weather in San Francisco on ")[1].split(" is stormy.")[0]
    datetime_obj = datetime.fromisoformat(datetime_str)
    datetime_now = datetime.now()
    assert datetime_now - datetime_obj < timedelta(milliseconds=100)
