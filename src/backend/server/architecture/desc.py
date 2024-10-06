from dataclasses import dataclass
from typing import Any, TypeAlias

from backend.server.architecture.layers.param import ParameterValue

LayerID: TypeAlias = str


@dataclass
class LayerDescription:
    id: LayerID
    input: LayerID | list[LayerID]
    param_values: dict[str, ParameterValue]

@dataclass
class ArchitectureDescription:
    layers: LayerDescription

