import pytest
import io
import os
import shutil
import tempfile
from uuid import uuid4
import zipfile
from typing import Generator, Tuple

import tomli_w

from vellum_cli.pull import pull_command


def zip_file_map(file_map: dict[str, str]) -> bytes:
    # Create an in-memory bytes buffer to store the zip
    zip_buffer = io.BytesIO()

    # Create zip file and add files from file_map
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in file_map.items():
            zip_file.writestr(filename, content)

    # Get the bytes from the buffer
    zip_bytes = zip_buffer.getvalue()
    zip_buffer.close()

    return zip_bytes


@pytest.fixture
def mock_module() -> Generator[Tuple[str, str], None, None]:
    current_dir = os.getcwd()
    temp_dir = tempfile.mkdtemp()
    os.chdir(temp_dir)
    module = "examples.mock"

    with open(os.path.join(temp_dir, "pyproject.toml"), "wb") as f:
        tomli_w.dump(
            {
                "tool": {
                    "vellum": {
                        "workflows": [
                            {
                                "module": module,
                                "workflow_sandbox_id": str(uuid4()),
                            }
                        ]
                    }
                }
            },
            f,
        )

    yield temp_dir, module

    os.chdir(current_dir)
    shutil.rmtree(temp_dir)


def test_pull(vellum_client, mock_module):
    # GIVEN a module on the user's filesystem
    temp_dir, module = mock_module

    # AND the workflow pull API call returns a zip file
    vellum_client.workflows.pull.return_value = iter([zip_file_map({"workflow.py": "print('hello')"})])

    # WHEN the user runs the pull command
    pull_command(module)

    # THEN the workflow.py file is written to the module directory
    assert os.path.exists(os.path.join(temp_dir, *module.split("."), "workflow.py"))
    with open(os.path.join(temp_dir, *module.split("."), "workflow.py")) as f:
        assert f.read() == "print('hello')"


def test_pull__remove_missing_files(vellum_client, mock_module):
    # GIVEN a module on the user's filesystem
    temp_dir, module = mock_module

    # AND the workflow pull API call returns a zip file
    vellum_client.workflows.pull.return_value = iter([zip_file_map({"workflow.py": "print('hello')"})])

    # AND there is already a different file in the module directory
    other_file_path = os.path.join(temp_dir, *module.split("."), "other_file.py")
    os.makedirs(os.path.dirname(other_file_path), exist_ok=True)
    with open(other_file_path, "w") as f:
        f.write("print('hello')")

    # WHEN the user runs the pull command
    pull_command(module)

    # THEN the workflow.py file is written to the module directory
    assert os.path.exists(os.path.join(temp_dir, *module.split("."), "workflow.py"))
    with open(os.path.join(temp_dir, *module.split("."), "workflow.py")) as f:
        assert f.read() == "print('hello')"

    # AND the other_file.py file is deleted
    assert not os.path.exists(other_file_path)


def test_pull__remove_missing_files__ignore_pattern(vellum_client, mock_module):
    # GIVEN a module on the user's filesystem
    temp_dir, module = mock_module

    # AND the workflow pull API call returns a zip file
    vellum_client.workflows.pull.return_value = iter([zip_file_map({"workflow.py": "print('hello')"})])

    # AND there is already a different file in the module directory
    other_file_path = os.path.join(temp_dir, *module.split("."), "other_file.py")
    os.makedirs(os.path.dirname(other_file_path), exist_ok=True)
    with open(other_file_path, "w") as f:
        f.write("print('hello')")

    # AND there is already a test file
    test_file_path = os.path.join(temp_dir, *module.split("."), "tests", "test_workflow.py")
    os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
    with open(test_file_path, "w") as f:
        f.write("print('hello')")

    # AND the ignore pattern is set to tests
    with open(os.path.join(temp_dir, "pyproject.toml"), "wb") as f:
        tomli_w.dump(
            {
                "tool": {
                    "vellum": {
                        "workflows": [
                            {
                                "module": module,
                                "workflow_sandbox_id": str(uuid4()),
                                "ignore": "tests/*",
                            }
                        ]
                    }
                }
            },
            f,
        )

    # WHEN the user runs the pull command
    pull_command(module)

    # THEN the workflow.py file is written to the module directory
    assert os.path.exists(os.path.join(temp_dir, *module.split("."), "workflow.py"))
    with open(os.path.join(temp_dir, *module.split("."), "workflow.py")) as f:
        assert f.read() == "print('hello')"

    # AND the other_file.py file is deleted
    assert not os.path.exists(other_file_path)

    # AND the tests/test_workflow.py file is untouched
    assert os.path.exists(test_file_path)


def test_pull__include_json(vellum_client, mock_module):
    # GIVEN a module on the user's filesystem
    _, module = mock_module

    # AND the workflow pull API call returns a zip file
    vellum_client.workflows.pull.return_value = iter(
        [zip_file_map({"workflow.py": "print('hello')", "workflow.json": "{}"})]
    )

    # WHEN the user runs the pull command
    pull_command(module, include_json=True)

    # THEN the pull api is called with include_json=True
    vellum_client.workflows.pull.assert_called_once()
    call_args = vellum_client.workflows.pull.call_args.kwargs
    assert call_args["request_options"]["additional_query_parameters"] == {"include_json": True}
