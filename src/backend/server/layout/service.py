from pathlib import Path

from server.architecture.config import ArchitectureConfig
from server.layout.config import LayoutConfig
from server.util.file.manager import BaseFileManager, JsonFileManager


class LayoutService:
    """
    A service for managing layout configurations and files.
    """

    files: BaseFileManager

    def __init__(self, save_path: Path) -> None:
        self.files = JsonFileManager(save_path, LayoutConfig, ".layout.json")
