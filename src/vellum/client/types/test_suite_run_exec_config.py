# This file was auto-generated by Fern from our API Definition.

import typing

from .test_suite_run_deployment_release_tag_exec_config import TestSuiteRunDeploymentReleaseTagExecConfig
from .test_suite_run_external_exec_config import TestSuiteRunExternalExecConfig
from .test_suite_run_prompt_sandbox_history_item_exec_config import TestSuiteRunPromptSandboxHistoryItemExecConfig
from .test_suite_run_workflow_release_tag_exec_config import TestSuiteRunWorkflowReleaseTagExecConfig
from .test_suite_run_workflow_sandbox_history_item_exec_config import TestSuiteRunWorkflowSandboxHistoryItemExecConfig

TestSuiteRunExecConfig = typing.Union[
    TestSuiteRunDeploymentReleaseTagExecConfig,
    TestSuiteRunPromptSandboxHistoryItemExecConfig,
    TestSuiteRunWorkflowReleaseTagExecConfig,
    TestSuiteRunWorkflowSandboxHistoryItemExecConfig,
    TestSuiteRunExternalExecConfig,
]
