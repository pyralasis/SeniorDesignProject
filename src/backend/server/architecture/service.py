from pathlib import Path

from server.architecture.config import ArchitectureConfig
from server.util.file.loaded import Loaded
from server.util.file.manager import BaseFileManager, JsonFileManager


class ArchitectureService:
    """
    A service for managing architecture configurations and files.
    """

    files: BaseFileManager[ArchitectureConfig]

    def __init__(self, save_path: Path) -> None:
        self.files = JsonFileManager(save_path, ArchitectureConfig, ".arch.json")
