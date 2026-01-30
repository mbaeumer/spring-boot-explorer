from pathlib import Path
from typing import Iterable, Set

def extract_unique_module_names(paths: Iterable[str], root_path: str) -> Set[str]:
    root = Path(root_path)

    first_folders = set()

    for p in paths:
        relative = Path(p).relative_to(root)
        first_folders.add(relative.parts[0])

    return first_folders