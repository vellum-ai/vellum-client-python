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
from src.vellum.lib.utils.paginator import PaginatedResults, get_all_results


class VellumTestSuiteRunExecution(TestSuiteRunExecution):
    @staticmethod
    def from_api(execution: TestSuiteRunExecution) -> VellumTestSuiteRunExecution:
        return VellumTestSuiteRunExecution(
            id=execution.id,
            test_case_id=execution.test_case_id,
            outputs=execution.outputs,
            metric_results=execution.metric_results,
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
        test_suite_run_id: str,
        client: Vellum | None = None,
        polling_inteval: int = DEFAULT_POLLING_INTERVAL_MS,
        max_polling_duration: int = DEFAULT_MAX_POLLING_DURATION_MS,
    ) -> None:
        self._test_suite_run_id = test_suite_run_id
        self._client = client or Vellum(
            api_key=os.environ.get("VELLUM_API_KEY"),
        )
        self._state = TestSuiteRunState.QUEUED
        self._executions: list[VellumTestSuiteRunExecution] | None = None
        self._polling_interval = polling_inteval
        self._max_polling_duration = max_polling_duration

    def get_metric_outputs(
        self, metric_identifier: str | None = None, output_identifier: str | None = None
    ) -> list[TestSuiteRunMetricOutput]:
        executions = self._get_test_suite_run_executions()

        return [
            execution.get_metric_output(metric_identifier=metric_identifier, output_identifier=output_identifier)
            for execution in executions
        ]

    def _refresh_test_suite_run_state(self):
        test_suite_run = self._client.test_suite_runs.retrieve(self._test_suite_run_id)
        self._state = test_suite_run.state

    def _list_paginated_executions(
        self, offset: int | None, limit: int | None
    ) -> PaginatedResults[TestSuiteRunExecution]:
        response = self._client.test_suite_runs.list_executions(
            self._test_suite_run_id,
            offset=offset,
            limit=limit,
            expand=["results.metric_results.metric_definition", "results.metric_results.metric_label"],
        )
        return PaginatedResults(results=response.results, count=response.count)

    def _get_test_suite_run_executions(self) -> list[VellumTestSuiteRunExecution]:
        if self._executions is not None:
            return self._executions

        start_time = time.time_ns()
        while True:
            self._refresh_test_suite_run_state()
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

        raw_api_executions = get_all_results(self._list_paginated_executions)
        self._executions = [VellumTestSuiteRunExecution.from_api(execution) for execution in raw_api_executions]
        return self._executions


class VellumTestSuite:
    def __init__(
        self,
        test_suite_id: str | None = None,
    ) -> None:
        self.client = Vellum(
            api_key=os.environ.get("VELLUM_API_KEY"),
        )
        self._test_suite_id = test_suite_id

    def run_external(
        self, executable: Callable[[list[TestCaseVariableValue]], list[NamedTestCaseVariableValueRequest]]
    ) -> VellumTestSuiteRunResults:
        """
        Runs this Vellum Test Suite on any executable function defined external to Vellum. Returns a results
        wrapper that polls the generated Test Suite Run for the latest metric results.
        """
        test_cases = self.client.test_suites.list_test_suite_test_cases(id=self._test_suite_id)
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
            test_suite_id=self._test_suite_id,
            exec_config=TestSuiteRunExternalExecConfigRequest(
                data=TestSuiteRunExternalExecConfigDataRequest(
                    executions=executions,
                ),
            ),
        )
        return VellumTestSuiteRunResults(test_suite_run.id)
