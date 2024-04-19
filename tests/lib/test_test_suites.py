from unittest.mock import Mock
from uuid import uuid4

from src.vellum.lib import VellumTestSuite
from src.vellum.types import (
    TestCaseVariableValue_String,
    TestCaseVariableValue_Json,
    NamedTestCaseVariableValueRequest_String,
    NamedTestCaseVariableValueRequest_Json,
    TestCaseVariableValue,
)
from pytest_httpx import HTTPXMock

# TODO: We should try to resolve this warning:
# src/vellum/types/test_case_variable_value.py:15
#   /Users/dvargas/vellum-ai/vellum-client-python/src/vellum/types/test_case_variable_value.py:15: \
#   PytestCollectionWarning: cannot collect test class 'TestCaseVariableValue_String' because it has a __init__ constructor (from: tests/lib/test_test_suites.py)
#     class TestCaseVariableValue_String(TestCaseStringVariableValue):


def test_vellum_test_suite__external__basic(httpx_mock: HTTPXMock) -> None:
    """Verify that the Vellum test suite can execute on external executions."""

    # GIVEN an external execution
    mock_execute_thing = Mock(
        # Less than ideal classes blocked on Fern: https://github.com/fern-api/fern/issues/2701
        return_value=[
            NamedTestCaseVariableValueRequest_String(name="output_a", value="Example string output"),
            NamedTestCaseVariableValueRequest_Json(name="output_b", value={"key": "value"}),
        ]
    )

    # AND a vellum test suite setup to handle that external eval
    test_suite_id = str(uuid4())
    input_variable_a_id = str(uuid4())
    input_variable_b_id = str(uuid4())
    example_test_suite = VellumTestSuite(id=test_suite_id)

    # AND the test suite is configured with relevant test cases
    test_case_id = str(uuid4())
    input_values: list[TestCaseVariableValue] = [
        TestCaseVariableValue_String(name="input_a", value="Example string input", variable_id=input_variable_a_id),
        TestCaseVariableValue_Json(name="input_b", value={"key": "value"}, variable_id=input_variable_b_id),
    ]
    httpx_mock.add_response(
        url=f"https://api.vellum.ai/v1/test-suites/{test_suite_id}/test-cases",
        method="GET",
        json={
            "count": 1,
            "results": [
                {
                    "id": test_case_id,
                    "input_values": [
                        {"variable_id": iv.variable_id, "name": iv.name, "type": iv.type, "value": iv.value}
                        for iv in input_values
                    ],
                    "evaluation_values": [],
                }
            ],
        },
    )

    # AND Vellum successfully evaluates the external execution
    test_suite_run_id = str(uuid4())
    test_suite_run_base = {
        "id": test_suite_run_id,
        "created": 0,
        "test_suite": {
            "id": test_suite_id,
            "history_item_id": str(uuid4()),
            "label": "Example Test Suite",
        },
    }
    httpx_mock.add_response(
        url="https://api.vellum.ai/v1/test-suite-runs",
        method="POST",
        json={
            **test_suite_run_base,
            "state": "QUEUED",
        },
    )
    httpx_mock.add_response(
        url=f"https://api.vellum.ai/v1/test-suite-runs/{test_suite_run_id}",
        method="GET",
        json={**test_suite_run_base, "state": "COMPLETE"},
    )
    httpx_mock.add_response(
        url=f"https://api.vellum.ai/v1/test-suite-runs/{test_suite_run_id}/executions?expand=results.metric_results.metric_definition&expand=results.metric_results.metric_label",
        method="GET",
        json={
            "count": 1,
            "results": [
                {
                    "id": str(uuid4()),
                    "test_case_id": test_case_id,
                    "outputs": [],
                    "metric_results": [
                        {
                            "metric_id": str(uuid4()),
                            "metric_label": "Exact Match",
                            "metric_definition": {"name": "exact_match", "id": str(uuid4()), "label": "Exact Match"},
                            "outputs": [{"name": "score", "value": 1.0, "type": "NUMBER"}],
                        },
                    ],
                },
            ],
        },
    )

    # WHEN the test suite is run
    results = example_test_suite.run_external(mock_execute_thing)

    # THEN the results should be as expected
    all_metrics = results.get_metric_outputs("exact_match", "score")

    assert all([mo.type == "NUMBER" and mo.value == 1.0 for mo in all_metrics])

    # AND the external executable should have been called
    # Fern doesn't yet support mock_execute_thing.assert_called_once_with(input_values)
    mock_execute_thing.assert_called_once()
    call_args = mock_execute_thing.call_args[0][0]
    for index, inp in enumerate(input_values):
        assert call_args[index].type == inp.type
        assert call_args[index].name == inp.name
        assert call_args[index].value == inp.value
        assert call_args[index].variable_id == inp.variable_id