from dataclasses import dataclass
from typing import Any, Protocol, TypeAlias

import torch
from server.layer.input import InputDefinition
from server.layer.size import TensorSize
from server.params import AnyParameter, Parameter

LayerID: TypeAlias = str


@dataclass
class LayerDescription:
    id: LayerID
    name: str
    inputs: tuple[InputDefinition, ...]
    parameters: tuple[AnyParameter, ...]


class LayerConstructor(Protocol):
    def __call__(self, in_sizes: tuple[TensorSize, ...], **params: Any) -> torch.nn.Module: ...


class LayerSizeCallable(Protocol):
    def __call__(self, in_sizes: tuple[TensorSize, ...], **params: Any) -> TensorSize: ...


@dataclass
class LayerDefinition:
    id: LayerID
    name: str
    inputs: tuple[InputDefinition, ...]
    parameters: tuple[AnyParameter, ...]
    constructor: LayerConstructor
    size: LayerSizeCallable

    def description(self) -> LayerDescription:
        return LayerDescription(self.id, self.name, self.inputs, self.parameters)
