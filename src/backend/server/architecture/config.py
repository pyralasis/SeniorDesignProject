from dataclasses import dataclass
from typing import TypeAlias

from server.params import ParameterValue
from server.layer import LayerID
from server.layer.size import TensorSize


LayerInstanceID: TypeAlias = int


@dataclass
class InputLayerConfig:
    id: LayerInstanceID
    size: TensorSize


@dataclass
class NetworkLayerConfig:
    id: LayerInstanceID
    layer_id: LayerID
    input: LayerInstanceID | list[LayerInstanceID]

    param_values: dict[str, ParameterValue]


@dataclass
class ArchitectureConfig:
    name: str
    inputs: list[InputLayerConfig]
    layers: list[NetworkLayerConfig]
