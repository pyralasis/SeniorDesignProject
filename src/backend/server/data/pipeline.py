from dataclasses import dataclass
from typing import TypeAlias

from server.data.sources import DataSourceId
from server.data.transforms import TransformId
from server.params import ParameterValue


InstanceId: TypeAlias = int


@dataclass
class SourceConfig:
    id: InstanceId
    src_id: DataSourceId
    param_values: dict[str, ParameterValue]


@dataclass
class TransformConfig:
    id: InstanceId
    transform_id: TransformId
    input: InstanceId | list[InstanceId]

    param_values: dict[str, ParameterValue]


@dataclass
class PipelineConfig:
    name: str
    sources: list[SourceConfig]
    transforms: list[TransformConfig]
    value_output: InstanceId
    label_output: InstanceId
