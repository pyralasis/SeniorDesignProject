
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generic, TypeVarTuple

import torch

from backend.server.architecture.layers.param import BoolParameter, IntParameter


T = TypeVarTuple("T")


@dataclass
class LayerDimensions:
    val: tuple[int, int]


class InputType(str, Enum):
    Single = "single"
    Multiple = "multiple"

@dataclass
class Layer(Generic[*T]):
    id: str
    input_type: InputType # We might need to rework this to support fixed size inputs
    parameters: tuple[*T]
    constructor: Callable[[LayerDimensions, *T], torch.nn.Module]



test = Layer[int, bool](
    "test",
    InputType.Single,
    (IntParameter("Number", 1), BoolParameter("Bool", True)),
    lambda dim, val, val2: torch.nn.Linear(10,10)
)