from pydantic.plugin import _loader as _pydantic_plugin_loader

from vellum.plugins.pydantic import pydantic_plugin

_loaded = False


def load_runtime_plugins() -> None:
    global _loaded
    if _loaded:
        return
    _loaded = True

    # TODO: This is a hack to get the Vellum plugin to load. We're supposed to use
    # pyproject.toml, but I couldn't figure out after an hour
    # https://app.shortcut.com/vellum/story/4635
    _pydantic_plugin_loader.get_plugins()
    if _pydantic_plugin_loader._plugins is not None:
        _pydantic_plugin_loader._plugins["vellum_plugin"] = pydantic_plugin
