from dataclasses import dataclass
from typing import Any, TypeAlias

from server.params import ParameterValue
from server.layer import LayerID
from server.layer.size import TensorSize


LayerInstanceID: TypeAlias = int


@dataclass
class InputLayerDescription:
    id: LayerInstanceID
    size: TensorSize


@dataclass
class NetworkLayerDescription:
    id: LayerInstanceID
    layer_id: LayerID
    input: LayerInstanceID | list[LayerInstanceID]

    param_values: dict[str, ParameterValue]


@dataclass
class ArchitectureDescription:
    name: str
    inputs: list[InputLayerDescription]
    layers: list[NetworkLayerDescription]
