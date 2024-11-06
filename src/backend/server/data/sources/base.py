from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Optional,
    Protocol,
    TypeAlias,
)

from click import Option


from server.params import (
    Parameter,
)


DatasetID: TypeAlias = str


DS_ROOT = "./datasets/"


class DataSourceConstructor(Protocol):
    def __call__(self, **params: Any) -> DataSource: ...


@dataclass
class DataSourceDefinition:
    id: DatasetID
    name: str
    parameters: tuple[Parameter[Any], ...]
    constructor: DataSourceConstructor


class DataSource(ABC):
    transform: Optional[Callable]

    def __init__(self) -> None:
        self.transform = None

    def set_transform(self, transform: Optional[Callable]) -> None:
        self.transform = transform

    def setup(self) -> None: ...

    @abstractmethod
    def _get(self, index: int) -> Any: ...

    def __getitem__(self, index: int) -> Any:
        if self.transform is None:
            return self._get(index)
        else:
            return self.transform(self._get(index))

    @abstractmethod
    def __len__(self) -> int: ...