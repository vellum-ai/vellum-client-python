import os
from typing import Union


def get_project_root() -> str:
    current_dir = os.getcwd()
    while current_dir != "/":
        if ".git" in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError("Project root not found.")


def find_file(project_root: str, filepath: str) -> str:
    # Early check if filepath is an absolute path
    if os.path.isabs(filepath):
        if os.path.exists(filepath):
            return filepath

    # Split the filepath into directories and the file name
    filepath_parts = filepath.split(os.sep)
    file_name = filepath_parts[-1]
    dir_path = os.sep.join(filepath_parts[:-1])

    for root, dirs, files in os.walk(project_root):
        # relative dir paths are for correct relative paths from root
        relative_dir_path = os.path.relpath(root, project_root)
        # non-relative dir paths are for incomplete paths from root
        non_relative_dir_path = os.path.basename(root)
        if (relative_dir_path == dir_path or non_relative_dir_path == dir_path) and file_name in files:
            return os.path.join(root, file_name)

    raise FileNotFoundError(f"File '{filepath}' not found in the project.")


def read_file_from_path(filepath: str) -> Union[str, None]:
    project_root = get_project_root()

    try:
        full_filepath = find_file(project_root, filepath)
    except FileNotFoundError:
        return None

    with open(full_filepath) as file:
        return file.read()
