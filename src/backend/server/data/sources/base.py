from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Optional, Protocol, TypeAlias

from server.params import Parameter
from torch.utils.data import Dataset

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


class DataSourceDataset(Dataset):
    def __init__(self, value_src: DataSource, label_src: DataSource) -> None:
        super().__init__()
        self.value_src = value_src
        self.label_src = label_src

    def __getitem__(self, i) -> Any:
        return (self.value_src[i], self.label_src[i])

    def __len__(self) -> int:
        return len(self.value_src)
