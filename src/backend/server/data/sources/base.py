from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Optional, Protocol, TypeAlias

from server.params import Parameter

DataSourceId: TypeAlias = str


DS_ROOT = "./datasets/"


@dataclass
class DataSourceDescription:
    id: DataSourceId
    name: str
    parameters: tuple[Parameter[Any], ...]


class DataSourceConstructor(Protocol):
    def __call__(self, **params: Any) -> DataSource: ...


@dataclass
class DataSourceDefinition:
    id: DataSourceId
    name: str
    parameters: tuple[Parameter[Any], ...]
    constructor: DataSourceConstructor

    def description(self) -> DataSourceDescription:
        return DataSourceDescription(self.id, self.name, self.parameters)


class DataSource(ABC):
    transforms: list[Callable]

    def __init__(self) -> None:
        self.transforms = []

    def add_transform(self, transform: Callable) -> None:
        self.transforms.append(transform)

    # TODO: Make a setup method?
    # @classmethod
    # def setup(cls) -> None: ...

    @abstractmethod
    def _get(self, index: int) -> Any: ...

    def __getitem__(self, index: int) -> Any:
        val = self._get(index)
        for transform in self.transforms:
            val = transform(val)
        return val

    @abstractmethod
    def __len__(self) -> int: ...
