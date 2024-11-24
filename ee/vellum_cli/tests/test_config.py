import os
import tempfile
from uuid import uuid4

from vellum_cli.config import VellumCliConfig, WorkflowConfig, load_vellum_cli_config


def test_load_vellum_cli_config__pyproject_toml_only():
    # GIVEN a pyproject.toml file with vellum config
    cwd = tempfile.mkdtemp()
    with open(os.path.join(cwd, "pyproject.toml"), "w") as f:
        f.write(
            """[[tool.vellum.workflows]]
module = "module1.workflow1"
"""
        )

    # WHEN the config is loaded
    config = load_vellum_cli_config(cwd)

    # THEN the config is loaded correctly
    assert config == VellumCliConfig(
        workflows=[WorkflowConfig(module="module1.workflow1")],
        version="1.0",
    )


def test_load_vellum_cli_config__pyproject_toml_and_lockfile():
    # GIVEN a pyproject.toml file with vellum config
    cwd = tempfile.mkdtemp()
    with open(os.path.join(cwd, "pyproject.toml"), "w") as f:
        f.write(
            """[[tool.vellum.workflows]]
module = "module1.workflow1"
"""
        )

    # AND a lockfile
    workflow_sandbox_id = uuid4()
    with open(os.path.join(cwd, "vellum.lock.json"), "w") as f:
        f.write(
            f"""{{
  "version": "1.0",
  "workflows": [
    {{
      "workflow_sandbox_id": "{workflow_sandbox_id}",
      "module": "module1.workflow1"
    }}
  ]
}}
"""
        )

    # WHEN the config is loaded
    config = load_vellum_cli_config(cwd)

    # THEN the config is loaded correctly
    assert config == VellumCliConfig(
        workflows=[WorkflowConfig(module="module1.workflow1", workflow_sandbox_id=str(workflow_sandbox_id))],
        version="1.0",
    )


def test_load_vellum_cli_config__pyproject_toml_and_lockfile__different_modules():
    # GIVEN a pyproject.toml file with vellum config
    cwd = tempfile.mkdtemp()
    with open(os.path.join(cwd, "pyproject.toml"), "w") as f:
        f.write(
            """[[tool.vellum.workflows]]
module = "module1.workflow1"
"""
        )

    # AND a lockfile
    workflow_sandbox_id = uuid4()
    with open(os.path.join(cwd, "vellum.lock.json"), "w") as f:
        f.write(
            f"""{{
  "version": "1.0",
  "workflows": [
    {{
      "workflow_sandbox_id": "{workflow_sandbox_id}",
      "module": "module2.workflow2"
    }}
  ]
}}
"""
        )

    # WHEN the config is loaded
    config = load_vellum_cli_config(cwd)

    # THEN the config is loaded correctly
    assert config == VellumCliConfig(
        workflows=[
            WorkflowConfig(module="module1.workflow1"),
            WorkflowConfig(module="module2.workflow2", workflow_sandbox_id=str(workflow_sandbox_id)),
        ],
        version="1.0",
    )
