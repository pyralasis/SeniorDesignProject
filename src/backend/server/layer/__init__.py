from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeAlias, TypeVar

import torch

from server.layer.input import InputDefinition
from server.layer.param import Parameter
from server.layer.size import TensorSize


T0 = TypeVar("T0")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")
T8 = TypeVar("T8")
T9 = TypeVar("T9")

LayerID: TypeAlias = str

LayerParameter: TypeAlias = (
    tuple[
        Parameter[T0],
        Parameter[T1],
        Parameter[T2],
        Parameter[T3],
        Parameter[T4],
        Parameter[T5],
        Parameter[T6],
        Parameter[T7],
        Parameter[T8],
        Parameter[T9],
    ]
    | tuple[
        Parameter[T0],
        Parameter[T1],
        Parameter[T2],
        Parameter[T3],
        Parameter[T4],
        Parameter[T5],
        Parameter[T6],
        Parameter[T7],
        Parameter[T8],
    ]
    | tuple[
        Parameter[T0],
        Parameter[T1],
        Parameter[T2],
        Parameter[T3],
        Parameter[T4],
        Parameter[T5],
        Parameter[T6],
        Parameter[T7],
    ]
    | tuple[
        Parameter[T0],
        Parameter[T1],
        Parameter[T2],
        Parameter[T3],
        Parameter[T4],
        Parameter[T5],
        Parameter[T6],
    ]
    | tuple[
        Parameter[T0],
        Parameter[T1],
        Parameter[T2],
        Parameter[T3],
        Parameter[T4],
        Parameter[T5],
    ]
    | tuple[Parameter[T0], Parameter[T1], Parameter[T2], Parameter[T3], Parameter[T4]]
    | tuple[Parameter[T0], Parameter[T1], Parameter[T2], Parameter[T3]]
    | tuple[Parameter[T0], Parameter[T1], Parameter[T2]]
    | tuple[Parameter[T0], Parameter[T1]]
    | tuple[Parameter[T0]]
    | tuple[()]
)

LayerConstructor: TypeAlias = (
    Callable[[TensorSize, T0, T1, T2, T3, T4, T5, T6, T7, T8, T9], torch.nn.Module]
    | Callable[[TensorSize, T0, T1, T2, T3, T4, T5, T6, T7, T8], torch.nn.Module]
    | Callable[[TensorSize, T0, T1, T2, T3, T4, T5, T6, T7], torch.nn.Module]
    | Callable[[TensorSize, T0, T1, T2, T3, T4, T5, T6], torch.nn.Module]
    | Callable[[TensorSize, T0, T1, T2, T3, T4, T5], torch.nn.Module]
    | Callable[[TensorSize, T0, T1, T2, T3, T4], torch.nn.Module]
    | Callable[[TensorSize, T0, T1, T2, T3], torch.nn.Module]
    | Callable[[TensorSize, T0, T1, T2], torch.nn.Module]
    | Callable[[TensorSize, T0, T1], torch.nn.Module]
    | Callable[[TensorSize, T0], torch.nn.Module]
    | Callable[[TensorSize], torch.nn.Module]
    | Callable[[], torch.nn.Module]
)


LayerSizeCalculator: TypeAlias = (
    Callable[[TensorSize, T0, T1, T2, T3, T4, T5, T6, T7, T8, T9], TensorSize]
    | Callable[[TensorSize, T0, T1, T2, T3, T4, T5, T6, T7, T8], TensorSize]
    | Callable[[TensorSize, T0, T1, T2, T3, T4, T5, T6, T7], TensorSize]
    | Callable[[TensorSize, T0, T1, T2, T3, T4, T5, T6], TensorSize]
    | Callable[[TensorSize, T0, T1, T2, T3, T4, T5], TensorSize]
    | Callable[[TensorSize, T0, T1, T2, T3, T4], TensorSize]
    | Callable[[TensorSize, T0, T1, T2, T3], TensorSize]
    | Callable[[TensorSize, T0, T1, T2], TensorSize]
    | Callable[[TensorSize, T0, T1], TensorSize]
    | Callable[[TensorSize, T0], TensorSize]
    | Callable[[TensorSize], TensorSize]
)


@dataclass
class LayerDescription:
    id: LayerID
    input: InputDefinition
    parameters: tuple[Parameter[Any], ...]


@dataclass
class Layer(Generic[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9]):
    id: LayerID
    input: InputDefinition  # We might need to rework this to support fixed size inputs
    parameters: LayerParameter[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9]
    constructor: LayerConstructor[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9]
    size: LayerSizeCalculator[T0, T1, T2, T3, T4, T5, T6, T7, T8, T9]

    def description(self) -> LayerDescription:
        return LayerDescription(self.id, self.input, self.parameters)
