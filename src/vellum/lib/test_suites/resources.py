from __future__ import annotations
import os
import time
from typing import Callable

from src.vellum.lib.test_suites.constants import DEFAULT_MAX_POLLING_DURATION_MS, DEFAULT_POLLING_INTERVAL_MS
from src.vellum.lib.test_suites.exceptions import TestSuiteRunResultsException
from src.vellum.types.named_test_case_variable_value_request import NamedTestCaseVariableValueRequest
from src.vellum.types.test_case_variable_value import TestCaseVariableValue
from src.vellum.client import Vellum
from src.vellum.types import (
    TestSuiteRunExecution,
    TestSuiteRunMetricOutput,
    TestSuiteRunState,
    TestSuiteRunExternalExecConfigRequest,
    TestSuiteRunExternalExecConfigDataRequest,
    ExternalTestCaseExecution,
)


class VellumTestSuiteRunExecution(TestSuiteRunExecution):
    @staticmethod
    def from_api(execution: TestSuiteRunExecution) -> VellumTestSuiteRunExecution:
        return VellumTestSuiteRunExecution(
            **execution,
        )

    def get_metric_output(
        self,
        metric_identifier: str | None = None,
        output_identifier: str | None = None,
    ) -> TestSuiteRunMetricOutput:
        metric_outputs = self.get_metric_outputs(metric_identifier)

        filtered_metric_outputs = [
            metric_output
            for metric_output in metric_outputs
            if not output_identifier or metric_output.name == output_identifier
        ]

        if len(filtered_metric_outputs) == 0:
            raise TestSuiteRunResultsException(f"No metric outputs found with identifier: {output_identifier}")

        if len(filtered_metric_outputs) > 1:
            raise TestSuiteRunResultsException(f"Multiple metric outputs found with identifier: {output_identifier}")

        return filtered_metric_outputs[0]

    def get_metric_outputs(
        self,
        metric_identifier: str | None = None,
    ) -> list[TestSuiteRunMetricOutput]:
        filtered_metric_results = [
            metric_output
            for metric_output in self.metric_results
            if not metric_identifier
            or (metric_output.metric_id == metric_identifier)
            or (metric_output.metric_label == metric_identifier)
            or (metric_output.metric_definition and metric_output.metric_definition.id == metric_identifier)
            or (metric_output.metric_definition and metric_output.metric_definition.name == metric_identifier)
            or (metric_output.metric_definition and metric_output.metric_definition.label == metric_identifier)
        ]

        if len(filtered_metric_results) == 0:
            raise TestSuiteRunResultsException(f"No metric results found with identifier: {metric_identifier}")

        if len(filtered_metric_results) > 1:
            raise TestSuiteRunResultsException(f"Multiple metric results found with identifier: {metric_identifier}")

        return filtered_metric_results[0].outputs


class VellumTestSuiteRunResults:
    def __init__(
        self,
        id: str,
        polling_inteval: int = DEFAULT_POLLING_INTERVAL_MS,
        max_polling_duration: int = DEFAULT_MAX_POLLING_DURATION_MS,
    ) -> None:
        self.id = id
        self.client = Vellum(
            api_key=os.environ.get("VELLUM_API_KEY"),
        )
        self._state = TestSuiteRunState.QUEUED
        self._executions: list[TestSuiteRunExecution] | None = None
        self._polling_interval = polling_inteval
        self._max_polling_duration = max_polling_duration

    def get_metric_outputs(
        self, metric_identifier: str | None = None, output_identifier: str | None = None
    ) -> list[TestSuiteRunMetricOutput]:
        executions = self._get_test_suite_run_executions()

        all_metric_results = [execution.metric_results for execution in executions]

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
            metric_output
            for metric_output_execution in filtered_metric_outputs
            for metric_output in metric_output_execution
            if not output_identifier or metric_output.name == output_identifier
        ]

        return [execution for execution in executions]

    def _refresh_test_suite_run(self):
        test_suite_run = self.client.test_suite_runs.retrieve(self.id)
        self._state = test_suite_run.state

    def _get_test_suite_run_executions(self):
        if self._executions is not None:
            return self._executions

        start_time = time.time_ns()
        while True:
            self._refresh_test_suite_run()
            if self._state not in {TestSuiteRunState.QUEUED, TestSuiteRunState.RUNNING}:
                break

            current_time = time.time_ns()
            if ((current_time - start_time) / 1e6) > self._max_polling_duration:
                raise TestSuiteRunResultsException("Test suite run timed out polling for executions")

            time.sleep(self._polling_interval / 1000.0)

        if self._state == TestSuiteRunState.FAILED:
            raise TestSuiteRunResultsException("Test suite run failed")

        if self._state == TestSuiteRunState.CANCELLED:
            raise TestSuiteRunResultsException("Test suite run was cancelled")

        response = self.client.test_suite_runs.list_executions(
            self.id, expand=["results.metric_results.metric_definition", "results.metric_results.metric_label"]
        )
        self._executions = response.results
        return self._executions


class VellumTestSuite:
    def __init__(
        self,
        id: str | None = None,
        # TODO: Support APIs that query by name
        # https://app.shortcut.com/vellum/story/2689
        # name: str | None = None,
    ) -> None:
        self.client = Vellum(
            api_key=os.environ.get("VELLUM_API_KEY"),
        )
        self._id = id

    def run_external(
        self, executable: Callable[[list[TestCaseVariableValue]], list[NamedTestCaseVariableValueRequest]]
    ) -> VellumTestSuiteRunResults:
        test_cases = self.client.test_suites.list_test_suite_test_cases(id=self._id)
        executions: list[ExternalTestCaseExecution] = []

        for test_case in test_cases.results:
            outputs = executable(test_case.input_values)

            executions.append(
                ExternalTestCaseExecution(
                    test_case_id=test_case.id,
                    outputs=outputs,
                )
            )

        test_suite_run = self.client.test_suite_runs.create(
            test_suite_id=self._id,
            exec_config=TestSuiteRunExternalExecConfigRequest(
                data=TestSuiteRunExternalExecConfigDataRequest(
                    executions=executions,
                ),
            ),
        )
        return VellumTestSuiteRunResults(test_suite_run.id)
