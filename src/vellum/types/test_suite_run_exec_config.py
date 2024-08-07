# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .test_suite_run_deployment_release_tag_exec_config_data import TestSuiteRunDeploymentReleaseTagExecConfigData
from .test_suite_run_external_exec_config_data import TestSuiteRunExternalExecConfigData
from .test_suite_run_workflow_release_tag_exec_config_data import TestSuiteRunWorkflowReleaseTagExecConfigData


class TestSuiteRunExecConfig_DeploymentReleaseTag(pydantic_v1.BaseModel):
    data: TestSuiteRunDeploymentReleaseTagExecConfigData
    test_case_ids: typing.Optional[typing.List[str]] = None
    type: typing.Literal["DEPLOYMENT_RELEASE_TAG"] = "DEPLOYMENT_RELEASE_TAG"

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}


class TestSuiteRunExecConfig_WorkflowReleaseTag(pydantic_v1.BaseModel):
    data: TestSuiteRunWorkflowReleaseTagExecConfigData
    test_case_ids: typing.Optional[typing.List[str]] = None
    type: typing.Literal["WORKFLOW_RELEASE_TAG"] = "WORKFLOW_RELEASE_TAG"

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}


class TestSuiteRunExecConfig_External(pydantic_v1.BaseModel):
    data: TestSuiteRunExternalExecConfigData
    test_case_ids: typing.Optional[typing.List[str]] = None
    type: typing.Literal["EXTERNAL"] = "EXTERNAL"

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}


TestSuiteRunExecConfig = typing.Union[
    TestSuiteRunExecConfig_DeploymentReleaseTag,
    TestSuiteRunExecConfig_WorkflowReleaseTag,
    TestSuiteRunExecConfig_External,
]
