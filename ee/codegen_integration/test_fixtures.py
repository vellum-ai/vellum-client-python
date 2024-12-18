import importlib


def test_fixtures__ensure_all_fixtures_are_importable(code_to_display_fixture_paths):
    """Confirms that all of our fixtures can be importable."""

    _, code_dir = code_to_display_fixture_paths
    base_module_path = __name__.split(".")[:-1]
    code_sub_path = code_dir.split("/".join(base_module_path))[1].split("/")[1:]
    module_path = ".".join(base_module_path + code_sub_path + ["workflow"])

    workflow = importlib.import_module(module_path)
    assert hasattr(workflow, "Workflow")
