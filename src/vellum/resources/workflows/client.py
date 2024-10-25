# This file was auto-generated by Fern from our API Definition.

import typing
from ...core.client_wrapper import SyncClientWrapper
from ...types.workflow_push_exec_config import WorkflowPushExecConfig
from ...core.request_options import RequestOptions
from ...types.workflow_push_response import WorkflowPushResponse
from ...core.pydantic_utilities import parse_obj_as
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class WorkflowsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def push(
        self,
        *,
        exec_config: WorkflowPushExecConfig,
        label: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> WorkflowPushResponse:
        """
        An internal-only endpoint that's subject to breaking changes without notice. Not intended for public use.

        Parameters
        ----------
        exec_config : WorkflowPushExecConfig

        label : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        WorkflowPushResponse


        Examples
        --------
        from vellum import Vellum

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.workflows.push(
            exec_config={"key": "value"},
            label="label",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/workflows/push",
            base_url=self._client_wrapper.get_environment().default,
            method="POST",
            json={
                "exec_config": exec_config,
                "label": label,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    WorkflowPushResponse,
                    parse_obj_as(
                        type_=WorkflowPushResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncWorkflowsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def push(
        self,
        *,
        exec_config: WorkflowPushExecConfig,
        label: str,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> WorkflowPushResponse:
        """
        An internal-only endpoint that's subject to breaking changes without notice. Not intended for public use.

        Parameters
        ----------
        exec_config : WorkflowPushExecConfig

        label : str

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        WorkflowPushResponse


        Examples
        --------
        import asyncio

        from vellum import AsyncVellum

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.workflows.push(
                exec_config={"key": "value"},
                label="label",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/workflows/push",
            base_url=self._client_wrapper.get_environment().default,
            method="POST",
            json={
                "exec_config": exec_config,
                "label": label,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    WorkflowPushResponse,
                    parse_obj_as(
                        type_=WorkflowPushResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
