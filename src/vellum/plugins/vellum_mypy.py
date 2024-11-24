from typing import Type

from mypy.plugin import Plugin


class VellumMypyPlugin(Plugin):
    pass


def plugin(version: str) -> Type[VellumMypyPlugin]:
    return VellumMypyPlugin
