import os
from typing import cast
import dotenv
from vellum.client import Vellum
from vellum.environment import VellumEnvironment
from vellum.lib.test_suites import VellumTestSuite
from vellum.types.named_test_case_variable_value_request import NamedTestCaseVariableValueRequest
from vellum.types.test_case_variable_value import TestCaseVariableValue
from vellum.types.workflow_request_input_request import WorkflowRequestInputRequest_String

dotenv.load_dotenv()

# Grab your `test_suite_id` from the Vellum UI
test_suite_id = "c8f4d490-4e99-4686-a6e2-4f4422daa218"

# Create a new VellumTestSuite object
test_suite = VellumTestSuite(test_suite_id=test_suite_id)

# Import the external execution from your code base
def external_execution(inputs: list[TestCaseVariableValue]) -> list[NamedTestCaseVariableValueRequest]:
    """We use a Vellum workflow as an example, but this could be _any_ prompt chain from your code base."""

    client = Vellum(api_key=cast(str, os.environ.get("VELLUM_API_KEY")))
    response = client.execute_workflow(
        inputs=inputs,  # type: ignore[arg-type]
        workflow_deployment_name="demo-external-workflow",
    )

    if response.data.state == "REJECTED":
        raise Exception(response.data.error.message)

    return response.data.outputs  # type: ignore[return-value]


# Run the external execution
results = test_suite.run_external(executable=external_execution)

# Verify the results
for result in results.get_metric_outputs("exact-match", "score"):
    assert result.value in [0.0, 1.0]
