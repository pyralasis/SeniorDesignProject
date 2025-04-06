from dataclasses import dataclass
from typing import Any, Literal, TypeAlias

from server.data.sources import DataSourceId
from server.data.sources.base import DataSourceDefinition
from server.data.transforms import TransformId
from server.data.transforms.base import TransformDefinition
from server.params import AnyParameter, AnyParameterValue, ParameterValue
from server.util.params import get_params_dict
from server.util.registry import Registry

InstanceId: TypeAlias = int


@dataclass
class SourceConfig:
    type: Literal["source"]
    instance_id: InstanceId
    src_id: DataSourceId
    param_values: list[tuple[str, AnyParameterValue]]

    def get_params(self) -> dict[str, Any]:
        return get_params_dict(self.param_values)


@dataclass
class TransformConfig:
    type: Literal["transform"]
    instance_id: InstanceId
    transform_id: TransformId
    input: InstanceId  # TODO: multiple inputs

    param_values: list[tuple[str, AnyParameterValue]]

    def get_params(self) -> dict[str, Any]:
        return get_params_dict(self.param_values)


PipelineElement: TypeAlias = SourceConfig | TransformConfig


@dataclass
class PipelineConfig:
    elements: list[PipelineElement]
    value_output: InstanceId
    label_output: InstanceId
