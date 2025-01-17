from pathlib import Path

from server.architecture.config import ArchitectureConfig
from server.util.file.manager import BaseFileManager, JsonFileManager


class ArchitectureService:
    files: BaseFileManager

    def __init__(self, save_path: Path) -> None:
        self.files = JsonFileManager(save_path, ArchitectureConfig, ".arch.json")
