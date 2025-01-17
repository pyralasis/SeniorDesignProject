from pathlib import Path

from server.data.pipeline import PipelineConfig
from server.data.sources import DataSourceDefinition
from server.data.transforms import TransformDefinition
from server.util.file.manager import JsonFileManager
from server.util.registry import Registry


class DataService:
    def __init__(
        self, save_path: Path, sources: list[DataSourceDefinition], transforms: list[TransformDefinition]
    ) -> None:
        self.pipelines = JsonFileManager(save_path, PipelineConfig, ".pipe.json")
        self.sources = Registry[DataSourceDefinition](sources)
        self.transforms = Registry[TransformDefinition](transforms)
