import pytest
import os
import shutil
import tempfile
from uuid import uuid4
from typing import Any, Callable, Dict, Generator, Tuple

import tomli_w


@pytest.fixture
def mock_module() -> Generator[Tuple[str, str, Callable[[Dict[str, Any]], None]], None, None]:
    current_dir = os.getcwd()
    temp_dir = tempfile.mkdtemp()
    os.chdir(temp_dir)
    module = "examples.mock"

    def set_pyproject_toml(vellum_config: Dict[str, Any]) -> None:
        pyproject_toml_path = os.path.join(temp_dir, "pyproject.toml")
        with open(pyproject_toml_path, "wb") as f:
            tomli_w.dump(
                {"tool": {"vellum": vellum_config}},
                f,
            )

    set_pyproject_toml(
        {
            "workflows": [
                {
                    "module": module,
                    "workflow_sandbox_id": str(uuid4()),
                }
            ]
        }
    )

    yield temp_dir, module, set_pyproject_toml

    os.chdir(current_dir)
    shutil.rmtree(temp_dir)
