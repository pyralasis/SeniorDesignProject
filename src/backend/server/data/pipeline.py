from dataclasses import dataclass
from typing import Any, Literal, TypeAlias

from server.data.sources import DataSourceId
from server.data.sources.base import DataSourceDefinition
from server.data.transforms import TransformId
from server.data.transforms.base import TransformDefinition
from server.params import AnyParameter, AnyParameterValue, ParameterValue
from server.util.registry import Registry

InstanceId: TypeAlias = int


@dataclass
class SourceConfig:
    type: Literal["source"]
    instance_id: InstanceId
    src_id: DataSourceId
    param_values: dict[str, AnyParameterValue]

    def get_params(self) -> dict[str, Any]:
        return {key: param.val for key, param in self.param_values.items()}


@dataclass
class TransformConfig:
    type: Literal["transform"]
    instance_id: InstanceId
    transform_id: TransformId
    input: InstanceId  # TODO: multiple inputs

    param_values: dict[str, AnyParameterValue]

    def get_params(self) -> dict[str, Any]:
        return {key: param.val for key, param in self.param_values.items()}


PipelineElement: TypeAlias = SourceConfig | TransformConfig


@dataclass
class PipelineConfig:
    elements: list[PipelineElement]
    value_output: InstanceId
    label_output: InstanceId
