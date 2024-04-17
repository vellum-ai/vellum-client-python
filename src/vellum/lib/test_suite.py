import os
import time
from typing import Any, Callable, Union
from uuid import uuid4
from ..client import Vellum
from ..types import (
    ChatMessage,
    NamedTestCaseJsonVariableValueRequest,
    NamedTestCaseNumberVariableValueRequest,
    NamedTestCaseStringVariableValueRequest,
    SearchResult,
    TestSuiteRunExecution,
    TestSuiteRunMetricOutput,
    TestSuiteRunState,
    VellumError,
    TestSuiteRunExternalExecConfigRequest,
    TestSuiteRunExternalExecConfigDataRequest,
    ExternalTestCaseExecution,
)


class VellumTestSuiteResults:
    def __init__(self, id: str) -> None:
        self.id = id
        self.client = Vellum(
            api_key=os.environ.get("VELLUM_API_KEY"),
        )
        self.test_suite_run_state = TestSuiteRunState.QUEUED
        self.test_suite_run_executions: list[TestSuiteRunExecution] | None = None

    def _refresh_test_suite_run_state(self):
        test_suite_run = self.client.test_suite_runs.retrieve(self.id)
        self.test_suite_run_state = test_suite_run.state

    def _ensure_metric_results_are_loaded(self):
        if self.test_suite_run_executions is not None:
            return

        self._refresh_test_suite_run_state()

        while self.test_suite_run_state in {TestSuiteRunState.QUEUED, TestSuiteRunState.RUNNING}:
            time.sleep(1)
            self._refresh_test_suite_run_state()
            # TODO: Max retries?

        if self.test_suite_run_state == TestSuiteRunState.FAILED:
            raise Exception("Test suite run failed")

        if self.test_suite_run_state == TestSuiteRunState.CANCELLED:
            raise Exception("Test suite run was cancelled")

        response = self.client.test_suite_runs.list_executions(
            self.id, expand=["results.metric_results.metric_definition"]
        )
        self.test_suite_run_executions = response.results

    def get_metric_outputs(
        self, metric_identifier: str | None = None, output_identifier: str | None = None
    ) -> list[list[TestSuiteRunMetricOutput]]:
        self._ensure_metric_results_are_loaded()

        all_metric_results = [execution.metric_results for execution in self.test_suite_run_executions]

        filtered_metric_outputs = [
            metric_result.outputs
            for metric_result_execution in all_metric_results
            for metric_result in metric_result_execution
            if not metric_identifier
            or (metric_result.metric_id == metric_identifier)
            or (metric_result.metric_label == metric_identifier)
            or (metric_result.metric_definition and metric_result.metric_definition.id == metric_identifier)
            or (metric_result.metric_definition and metric_result.metric_definition.name == metric_identifier)
            or (metric_result.metric_definition and metric_result.metric_definition.label == metric_identifier)
        ]

        filtered_metric_filtered_outputs = [
            [
                metric_output
                for metric_output in metric_output_execution
                if not output_identifier
                or metric_output.name == output_identifier
            ]
            for metric_output_execution in filtered_metric_outputs
        ]

        return filtered_metric_filtered_outputs


ValidOutput = Union[
    str,
    float,
    dict[str, Any],
    list[SearchResult],
    list[ChatMessage],
    VellumError,
]


class VellumTestSuite:
    def __init__(self, name: str) -> None:
        self.name = name
        self.client = Vellum(
            api_key=os.environ.get("VELLUM_API_KEY"),
        )
        self.test_suite_id = self._get_test_suite_id_by_name(name)

    def _get_test_suite_id_by_name(self, name: str) -> str:
        # TODO: We need to EITHER:
        # - Allow for all of these methods to be called with `name`
        # - OR, we need to expose a get test suite id by name method and save the `id`
        return uuid4()

    def run_external(self, external_evaluator: Callable[..., dict[str, ValidOutput]]) -> VellumTestSuiteResults:
        test_cases = self.client.test_suites.list_test_suite_test_cases(id=self.test_suite_id)
        executions: list[ExternalTestCaseExecution] = []

        # TODO - we need either:
        # - Retrieve input_variables[i].key from test_suites
        # - OR add a `name` field to `TestCaseVariableValue`
        input_variable_name_by_id = {}

        for test_case in test_cases.results:
            inputs = test_case.input_values
            external_input = {input_variable_name_by_id.get(inp.variable_id): inp.value for inp in inputs}
            external_outputs = external_evaluator(
                **external_input,
            )

            outputs = []
            for external_output_key, external_output_value in external_outputs.items():
                if isinstance(external_output_value, str):
                    # Doesn't currently work - requires NamedTestCaseVariableValueRequest_String
                    # Same for all other options below
                    outputs.append(
                        NamedTestCaseStringVariableValueRequest(
                            value=external_output_value,
                            name=external_output_key,
                        )
                    )

                elif isinstance(external_output_value, float):
                    outputs.append(
                        NamedTestCaseNumberVariableValueRequest(
                            value=external_output_value,
                            name=external_output_key,
                        )
                    )

                elif isinstance(external_output_value, dict):
                    outputs.append(
                        NamedTestCaseJsonVariableValueRequest(
                            value=external_output_value,
                            name=external_output_key,
                        )
                    )

                # TODO: Handle the rest of the types

            executions.append(
                ExternalTestCaseExecution(
                    test_case_id=test_case.id,
                    outputs=outputs,
                )
            )

        test_suite_run = self.client.test_suite_runs.create(
            test_suite_id=self.test_suite_id,
            # TODO: Also doesn't work yet for the same reason as variables above
            exec_config=TestSuiteRunExternalExecConfigRequest(
                data=TestSuiteRunExternalExecConfigDataRequest(
                    executions=executions,
                ),
            ),
        )
        return VellumTestSuiteResults(test_suite_run.id)
