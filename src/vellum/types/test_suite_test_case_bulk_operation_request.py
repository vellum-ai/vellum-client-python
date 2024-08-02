# This file was auto-generated by Fern from our API Definition.

from __future__ import annotations

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .create_test_suite_test_case_request import CreateTestSuiteTestCaseRequest
from .replace_test_suite_test_case_request import ReplaceTestSuiteTestCaseRequest
from .test_suite_test_case_delete_bulk_operation_data_request import TestSuiteTestCaseDeleteBulkOperationDataRequest
from .upsert_test_suite_test_case_request import UpsertTestSuiteTestCaseRequest


class TestSuiteTestCaseBulkOperationRequest_Create(pydantic_v1.BaseModel):
    id: str
    data: CreateTestSuiteTestCaseRequest
    type: typing.Literal["CREATE"] = "CREATE"

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


class TestSuiteTestCaseBulkOperationRequest_Replace(pydantic_v1.BaseModel):
    id: str
    data: ReplaceTestSuiteTestCaseRequest
    type: typing.Literal["REPLACE"] = "REPLACE"

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


class TestSuiteTestCaseBulkOperationRequest_Upsert(pydantic_v1.BaseModel):
    id: str
    data: UpsertTestSuiteTestCaseRequest
    type: typing.Literal["UPSERT"] = "UPSERT"

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


class TestSuiteTestCaseBulkOperationRequest_Delete(pydantic_v1.BaseModel):
    id: str
    data: TestSuiteTestCaseDeleteBulkOperationDataRequest
    type: typing.Literal["DELETE"] = "DELETE"

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


TestSuiteTestCaseBulkOperationRequest = typing.Union[
    TestSuiteTestCaseBulkOperationRequest_Create,
    TestSuiteTestCaseBulkOperationRequest_Replace,
    TestSuiteTestCaseBulkOperationRequest_Upsert,
    TestSuiteTestCaseBulkOperationRequest_Delete,
]
