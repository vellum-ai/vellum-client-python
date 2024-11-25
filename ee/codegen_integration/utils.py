import glob
import os
import re
from typing import List, Optional


def get_all_files_in_dir(dir_path: str, ignore_regexes: Optional[List[re.Pattern]] = None) -> List[str]:
    files: List[str] = []
    for f in glob.glob(f"{dir_path}/**", recursive=True):
        if not os.path.isfile(f):
            continue
        if ignore_regexes and any(regex.match(f) for regex in ignore_regexes):
            continue

        files.append(os.path.relpath(f, dir_path))

    return files
