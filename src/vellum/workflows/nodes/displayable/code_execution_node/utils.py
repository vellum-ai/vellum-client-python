import os
from typing import Union


def read_file_from_path(node_filepath: str, script_filepath: str) -> Union[str, None]:
    node_filepath_dir = os.path.dirname(node_filepath)
    full_filepath = os.path.join(node_filepath_dir, script_filepath)

    if os.path.isfile(full_filepath):
        with open(full_filepath) as file:
            return file.read()
    return None
