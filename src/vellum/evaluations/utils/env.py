import os

from .exceptions import VellumClientException


def get_api_key() -> str:
    api_key = os.environ.get("VELLUM_API_KEY")
    if api_key is None:
        raise VellumClientException("`VELLUM_API_KEY` environment variable is required to be set.")

    return api_key
