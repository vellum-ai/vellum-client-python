from __future__ import annotations
import logging
import time
from typing import Callable, Generator

from .constants import DEFAULT_MAX_POLLING_DURATION_MS, DEFAULT_POLLING_INTERVAL_MS
from .exceptions import TestSuiteRunResultsException
from ..utils.env import get_api_key
from ...client import Vellum
from ...types import (
    ExternalTestCaseExecutionRequest,
    NamedTestCaseVariableValueRequest,
    TestCaseVariableValue,
    TestSuiteRunExecution,
    TestSuiteRunMetricOutput,
    TestSuiteRunState,
    TestSuiteRunExecConfigRequest_External,
    TestSuiteRunExternalExecConfigDataRequest,
)
from ..utils.paginator import PaginatedResults, get_all_results

logger = logging.getLogger(__name__)


class VellumTestSuiteRunExecution(TestSuiteRunExecution):
    @classmethod
    def from_api(cls, execution: TestSuiteRunExecution) -> VellumTestSuiteRunExecution:
        return cls(
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
        """Retrieve a metric's output by specifying the info needed to uniquely identify that metric and output."""

        metric_outputs = self.get_metric_outputs(metric_identifier)

        filtered_metric_outputs = [
            metric_output
            for metric_output in metric_outputs
            if output_identifier is None or metric_output.name == output_identifier
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
        """Return a metric's output across all executions by providing the info needed to uniquely identify that metric."""

        filtered_metric_results = [
            metric_output
            for metric_output in self.metric_results
            if metric_identifier is None
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
        *,
        client: Vellum | None = None,
        polling_inteval: int = DEFAULT_POLLING_INTERVAL_MS,
        max_polling_duration: int = DEFAULT_MAX_POLLING_DURATION_MS,
    ) -> None:
        self._test_suite_run_id = test_suite_run_id
        self._client = client or Vellum(
            api_key=get_api_key(),
        )
        self._state = TestSuiteRunState.QUEUED
        self._executions: Generator[VellumTestSuiteRunExecution, None, None] | None = None
        self._polling_interval = polling_inteval
        self._max_polling_duration = max_polling_duration

    def get_metric_outputs(
        self, metric_identifier: str | None = None, output_identifier: str | None = None
    ) -> Generator[TestSuiteRunMetricOutput, None, None]:
        executions = self._get_test_suite_run_executions()

        for execution in executions:
            yield execution.get_metric_output(metric_identifier=metric_identifier, output_identifier=output_identifier)

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

    def _wrap_api_executions(
        self, executions: Generator[TestSuiteRunExecution, None, None]
    ) -> Generator[VellumTestSuiteRunExecution, None, None]:
        for execution in executions:
            yield VellumTestSuiteRunExecution.from_api(execution)

    def _get_test_suite_run_executions(self) -> Generator[VellumTestSuiteRunExecution, None, None]:
        if self._executions is not None:
            return self._executions

        start_time = time.time_ns()
        while True:
            logger.debug("Polling for latest test suite run state...")
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
        self._executions = self._wrap_api_executions(raw_api_executions)
        return self._executions


class VellumTestSuite:
    def __init__(
        self,
        test_suite_id: str,
        *,
        client: Vellum | None = None,
    ) -> None:
        self.client = client or Vellum(
            api_key=get_api_key(),
        )
        self._test_suite_id = test_suite_id

    def run_external(
        self, executable: Callable[[list[TestCaseVariableValue]], list[NamedTestCaseVariableValueRequest]]
    ) -> VellumTestSuiteRunResults:
        """
        Runs this Vellum Test Suite on any executable function defined external to Vellum.

        Returns a results wrapper that polls the generated Test Suite Run for the latest metric results.
        """
        test_cases = self.client.test_suites.list_test_suite_test_cases(id=self._test_suite_id)
        executions: list[ExternalTestCaseExecutionRequest] = []

        for test_case in test_cases.results:
            outputs = executable(test_case.input_values)

            executions.append(
                ExternalTestCaseExecutionRequest(
                    test_case_id=test_case.id,  # type: ignore[arg-type]
                    outputs=outputs,
                )
            )

        test_suite_run = self.client.test_suite_runs.create(
            test_suite_id=self._test_suite_id,
            exec_config=TestSuiteRunExecConfigRequest_External(
                data=TestSuiteRunExternalExecConfigDataRequest(
                    executions=executions,
                ),
            ),
        )
        return VellumTestSuiteRunResults(test_suite_run.id, client=self.client)
