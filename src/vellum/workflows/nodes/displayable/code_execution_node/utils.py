import os
from typing import Union


def read_file_from_path(filepath: str) -> Union[str, None]:
    if not os.path.exists(filepath):
        return None

    with open(filepath) as file:
        return file.read()
