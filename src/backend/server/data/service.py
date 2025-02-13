from dataclasses import dataclass
from pathlib import Path
from typing import cast

from server.data.pipeline import (
    InstanceId,
    PipelineConfig,
    PipelineElement,
    SourceConfig,
    TransformConfig,
)
from server.data.sources import DataSourceDefinition
from server.data.sources.base import DataSource
from server.data.transforms import TransformDefinition
from server.data.transforms.base import (
    DataSourceTransformDefinition,
    ValueTransformDefinition,
)
from server.layout import LayoutConfig, create_layout_file_manager
from server.params import BoolParameterValue, IntParameterValue
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

    def config_to_sources(self, config: PipelineConfig) -> tuple[DataSource, DataSource]:
        """
        Converts a PipelineConfig into DataSources.
        Returns value source and label source in that order.
        """

        node_map: dict[InstanceId, PipelineElement] = {}
        for el in config.elements:
            node_map[el.instance_id] = el

        def get_source_for(id: InstanceId):
            el = node_map[id]

            if el.type == "source":
                return self.sources.get(el.src_id).constructor(**el.param_values)
            else:
                source = get_source_for(el.input)
                transform_type = self.transforms.get(el.transform_id)
                if transform_type.type() == "datasource_transform":
                    transform_type = cast(DataSourceTransformDefinition, transform_type)
                    return transform_type.constructor(source, **el.get_params())
                else:
                    transform_type = cast(ValueTransformDefinition, transform_type)
                    source.add_transform(transform_type.constructor(**el.get_params()))
                    return source

        value_source = get_source_for(config.value_output)
        label_source = get_source_for(config.label_output)

        return value_source, label_source
