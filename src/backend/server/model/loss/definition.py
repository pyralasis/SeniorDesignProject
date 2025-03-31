from dataclasses import dataclass
from typing import Any, Protocol, TypeAlias

import torch
from server.params import AnyParameter

LossID: TypeAlias = str


@dataclass
class LossDescription:
    id: LossID
    name: str
    parameters: tuple[AnyParameter, ...]


class LossConstructor(Protocol):
    def __call__(self, **params: Any) -> torch.nn.Module: ...


@dataclass
class LossDefinition:
    id: LossID
    name: str
    parameters: tuple[AnyParameter, ...]
    constructor: LossConstructor

    def description(self) -> LossDescription:
        return LossDescription(self.id, self.name, self.parameters)
