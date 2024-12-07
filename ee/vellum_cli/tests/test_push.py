from click.testing import CliRunner

from vellum_cli import main as cli_main


def test_push__no_config(mock_module):
    # GIVEN no config file set
    _, _, set_pyproject_toml = mock_module
    set_pyproject_toml({"workflows": []})

    # WHEN calling `vellum push`
    runner = CliRunner()
    result = runner.invoke(cli_main, ["push"])

    # THEN it should fail
    assert result.exit_code == 1
    assert result.exception
    assert str(result.exception) == "No Workflows found in project to push."


def test_push__multiple_workflows_configured__no_module_specified(mock_module):
    # GIVEN multiple workflows configured
    _, _, set_pyproject_toml = mock_module
    set_pyproject_toml({"workflows": [{"module": "examples.mock"}, {"module": "examples.mock2"}]})

    # WHEN calling `vellum push` without a module specified
    runner = CliRunner()
    result = runner.invoke(cli_main, ["push"])

    # THEN it should fail
    assert result.exit_code == 1
    assert result.exception
    assert (
        str(result.exception)
        == "Multiple workflows found in project to push. Pushing only a single workflow is supported."
    )


def test_push__multiple_workflows_configured__not_found_module(mock_module):
    # GIVEN multiple workflows configured
    _, module, set_pyproject_toml = mock_module
    set_pyproject_toml({"workflows": [{"module": "examples.mock2"}, {"module": "examples.mock3"}]})

    # WHEN calling `vellum push` with a module that doesn't exist
    runner = CliRunner()
    result = runner.invoke(cli_main, ["push", module])

    # THEN it should fail
    assert result.exit_code == 1
    assert result.exception
    assert str(result.exception) == f"No workflow config for '{module}' found in project to push."
