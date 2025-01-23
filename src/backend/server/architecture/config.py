from dataclasses import dataclass
from typing import TypeAlias

from server.params import ParameterValue
from server.layer import LayerDefinition, LayerID
from server.layer.size import TensorSize
from server.util.registry import Registry


# This can be any number as long as all layer instance ids within an architecture are unique.
LayerInstanceID: TypeAlias = int


@dataclass
class InputLayerConfig:
    """An input to an architecture."""

    id: LayerInstanceID
    size: TensorSize


@dataclass
class NetworkLayerConfig:
    """A layer within an architecture."""

    id: LayerInstanceID
    layer_id: LayerID  # The ID of the layer type
    input: LayerInstanceID | list[LayerInstanceID]  # The layer or input that feeds into this network.

    param_values: dict[str, ParameterValue]  # the values for each parameter in the layer


@dataclass
class ArchitectureConfig:
    """
    Configuration class for defining the architecture of a neural network. This is the data
    structure that gets saved to disk for each architecture.
    """

    name: str
    version: int
    inputs: list[InputLayerConfig]
    layers: list[NetworkLayerConfig]

    layout_file: str | None
