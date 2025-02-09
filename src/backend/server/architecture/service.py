from dataclasses import dataclass
from pathlib import Path

from server.architecture.config import ArchitectureConfig
from server.layout import LayoutConfig, create_layout_file_manager
from server.util.file import (
    BaseFileManager,
    FileCoordinator,
    FileId,
    JsonFileManager,
    Loadable,
    MetaData,
)


@dataclass
class ArchitectureObject(Loadable):
    meta: MetaData
    data: ArchitectureConfig
    layout: LayoutConfig


class ArchitectureService:
    """
    A service for managing architecture configurations and files.
    """

    architectures: FileCoordinator[ArchitectureObject, ArchitectureConfig, LayoutConfig]

    def __init__(self, save_path: Path) -> None:
        self.architectures = FileCoordinator(
            ArchitectureObject,
            "architecture",
            JsonFileManager("data", save_path, ArchitectureConfig, ".arch.json"),
            [create_layout_file_manager(save_path)],
            save_path,
        )

    def load_architecture(self, architecture_id: FileId) -> ArchitectureConfig:
        return self.architectures.data_files.load(architecture_id)
