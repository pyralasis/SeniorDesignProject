from pathlib import Path

from server.architecture.config import ArchitectureConfig
from server.util.file.manager import FileManager


class ArchitectureService:
    files: FileManager

    def __init__(self, save_path: Path) -> None:
        self.files = FileManager(save_path, ArchitectureConfig)
