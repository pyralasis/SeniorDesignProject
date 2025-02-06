from dataclasses import dataclass
from typing import Any, Protocol, TypeAlias

import torch

from server.layer.input import InputDefinition
from server.params import (
    Parameter,
)
from server.layer.size import TensorSize


LayerID: TypeAlias = str


@dataclass
class LayerDescription:
    id: LayerID
    name: str
    inputs: tuple[InputDefinition, ...]
    parameters: tuple[Parameter[Any], ...]


class LayerConstructor(Protocol):
    def __call__(self, in_sizes: tuple[TensorSize, ...], **params: Any) -> torch.nn.Module: ...


class LayerSizeCallable(Protocol):
    def __call__(self, in_sizes: tuple[TensorSize, ...], **params: Any) -> TensorSize: ...


@dataclass
class ParameterValue:
    val: Any
    type: str


@dataclass
class LayerDefinition:
    id: LayerID
    name: str
    inputs: tuple[InputDefinition, ...]
    parameters: tuple[Parameter[Any], ...]
    constructor: LayerConstructor
    size: LayerSizeCallable

    def description(self) -> LayerDescription:
        return LayerDescription(self.id, self.name, self.inputs, self.parameters)
