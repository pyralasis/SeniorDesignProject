from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Literal,
    Protocol,
    TypeAlias,
    TypeVar,
)

from server.data.sources.base import DataSource
from server.params import Parameter


TransformID: TypeAlias = str

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


@dataclass
class TransformDescription:
    type: Literal["value_transform"] | Literal["datasource_transform"]
    id: TransformID
    name: str


class ValueTransformConstructor(Protocol):
    def __call__(self, **params: Any) -> Callable[..., Any]: ...


@dataclass
class ValueTransformDefinition:
    id: TransformID
    name: str
    parameters: tuple[Parameter[Any], ...]
    constructor: ValueTransformConstructor

    def description(self) -> TransformDescription:
        return TransformDescription(self.type(), self.id, self.name)

    @classmethod
    def type(cls) -> Literal["value_transform"]:
        return "value_transform"


class DataSourceTransformConstructor(Protocol):
    def __call__(self, source: DataSource, **params: Any) -> DataSource: ...


@dataclass
class DataSourceTransformDefinition:
    id: TransformID
    name: str
    parameters: tuple[Parameter[Any], ...]
    constructor: DataSourceTransformConstructor

    def description(self) -> TransformDescription:
        return TransformDescription(self.type(), self.id, self.name)

    @classmethod
    def type(cls) -> Literal["datasource_transform"]:
        return "datasource_transform"
