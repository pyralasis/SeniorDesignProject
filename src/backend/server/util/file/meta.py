from pathlib import Path
from typing import Any, TypeAlias

from server.util.file.manager import JsonFileManager

MetaData: TypeAlias = dict[str, Any]


def create_meta_file_manager(save_path: Path):
    return JsonFileManager("meta", save_path, MetaData, ".meta.json")
