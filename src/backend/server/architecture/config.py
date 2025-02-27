from dataclasses import dataclass
from typing import Any, TypeAlias

from server.layer import LayerID
from server.layer.size import TensorSize
from server.params import ParameterValue

# This can be any number as long as all layer instance ids within an architecture are unique.
LayerInstanceID: TypeAlias = int


@dataclass
class InputLayerConfig:
    """An input to an architecture."""

    instance_id: LayerInstanceID
    size: TensorSize


@dataclass
class NetworkLayerConfig:
    """A layer within an architecture."""

    instance_id: LayerInstanceID  # a unique identifier for this layer instance
    layer_id: LayerID  # The ID of the layer type
    input: list[LayerInstanceID]  # The layer or input that feeds into this network.

    param_values: dict[str, ParameterValue]  # the values for each parameter in the layer

    def get_params(self) -> dict[str, Any]:
        return {key: param.val for key, param in self.param_values.items()}


@dataclass
class ArchitectureConfig:
    """
    Configuration class for defining the architecture of a neural network. This is the data
    structure that gets saved to disk for each architecture.
    """

    inputs: list[InputLayerConfig]
    layers: list[NetworkLayerConfig]
    output: LayerInstanceID  # id of layers that are outputs
