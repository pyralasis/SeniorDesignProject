from dataclasses import dataclass
from typing import Any, Protocol, TypeAlias

import torch
from server.params import AnyParameter

OptimID: TypeAlias = str


@dataclass
class OptimizerDescription:
    id: OptimID
    name: str
    parameters: tuple[AnyParameter, ...]


class OptimizerConstructor(Protocol):
    def __call__(self, model: torch.nn.Module, **params: Any) -> torch.optim.Optimizer: ...


@dataclass
class OptimizerDefinition:
    id: OptimID
    name: str
    parameters: tuple[AnyParameter, ...]
    constructor: OptimizerConstructor

    def description(self) -> OptimizerDescription:
        return OptimizerDescription(self.id, self.name, self.parameters)
