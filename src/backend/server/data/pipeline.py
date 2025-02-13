from dataclasses import dataclass
from typing import Literal, TypeAlias

from server.data.sources import DataSourceId
from server.data.sources.base import DataSourceDefinition
from server.data.transforms import TransformId
from server.data.transforms.base import TransformDefinition
from server.params import ParameterValue
from server.util.registry import Registry

InstanceId: TypeAlias = int


@dataclass
class SourceConfig:
    type: Literal["source"]
    instance_id: InstanceId
    src_id: DataSourceId
    param_values: dict[str, ParameterValue]


@dataclass
class TransformConfig:
    type: Literal["transform"]
    instance_id: InstanceId
    transform_id: TransformId
    input: list[InstanceId]

    param_values: dict[str, ParameterValue]


@dataclass
class PipelineConfig:
    elements: list[SourceConfig | TransformConfig]
    value_output: InstanceId
    label_output: InstanceId
