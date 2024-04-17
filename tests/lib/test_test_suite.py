from typing import Any
from uuid import uuid4
from ...src.vellum.lib import VellumTestSuite
import pytest
from requests_mock import Mocker as RequestsMocker


# Get started with writing tests with pytest at https://docs.pytest.org
@pytest.mark.skip(reason="This test is not yet implemented")
def test_vellum_test_suite__external__basic(requests_mock: RequestsMocker) -> None:
    """Verify that the Vellum test suite could execute on External executions."""

    # GIVEN an external execution
    def mock_execute_thing(input_a: str, input_b: dict[str, Any]) -> dict[str, Any]:
        """This could be the invocation of a Prompt, Langchain chain, etc."""

        return {"output_a": "Example string output", "output_b": {"key": "value"}}

    # AND a vellum test suite setup to handle that external eval
    # - Note that with TestSuites as code, we could define the test suite inline
    example_test_suite = VellumTestSuite("example_test_suite")

    # AND Vellum successfully evaluates the external execution
    test_suite_run_id = uuid4()
    requests_mock.post(url="https://api.vellum.ai/v1/test_suite_runs")
    requests_mock.get(
        url=f"https://api.vellum.ai/v1/test_suite_runs/{test_suite_run_id}/executions?expand[0]=results.metric_results.metric_definition",
    )

    # WHEN the test suite is run
    results = example_test_suite.run_external(mock_execute_thing)

    # THEN the results should be as expected
    all_metrics = results.get_metric_outputs("exact_match")
    a_metrics = results.get_metric_outputs("exact_match", "output_a")
    b_metrics = results.get_metric_outputs("exact_match", "output_b")

    assert len(all_metrics) == len(a_metrics) + len(b_metrics)
    assert all([mo.type == "NUMBER" and mo.value == 1.0 for mo in all_metrics])
