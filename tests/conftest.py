# This file was auto-generated by Fern from our API Definition.

from vellum import Vellum
import os
from vellum.environment import VellumEnvironment
import pytest
from vellum import AsyncVellum


@pytest.fixture
def client() -> Vellum:
    return Vellum(
        api_key=os.getenv("ENV_API_KEY", "api_key"),
        environment=VellumEnvironment(
            default=os.getenv("TESTS_BASE_URL", "base_url"),
            documents=os.getenv("TESTS_BASE_URL", "base_url"),
            predict=os.getenv("TESTS_BASE_URL", "base_url"),
        ),
    )


@pytest.fixture
def async_client() -> AsyncVellum:
    return AsyncVellum(
        api_key=os.getenv("ENV_API_KEY", "api_key"),
        environment=VellumEnvironment(
            default=os.getenv("TESTS_BASE_URL", "base_url"),
            documents=os.getenv("TESTS_BASE_URL", "base_url"),
            predict=os.getenv("TESTS_BASE_URL", "base_url"),
        ),
    )
