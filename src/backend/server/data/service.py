from dataclasses import dataclass
from pathlib import Path

from server.data.pipeline import PipelineConfig
from server.data.sources import DataSourceDefinition
from server.data.transforms import TransformDefinition
from server.layout import LayoutConfig, create_layout_file_manager
from server.util.file import FileCoordinator, JsonFileManager, Loadable, MetaData
from server.util.registry import Registry


@dataclass
class PipelineObject(Loadable):
    meta: MetaData
    data: PipelineConfig
    layout: LayoutConfig


class DataService:
    def __init__(
        self, save_path: Path, sources: list[DataSourceDefinition], transforms: list[TransformDefinition]
    ) -> None:
        self.pipelines = FileCoordinator(
            PipelineObject,
            "pipeline",
            JsonFileManager("data", save_path, PipelineConfig, ".pipe.json"),
            [create_layout_file_manager(save_path)],
            save_path,
        )
        self.sources = Registry[DataSourceDefinition](sources)
        self.transforms = Registry[TransformDefinition](transforms)
