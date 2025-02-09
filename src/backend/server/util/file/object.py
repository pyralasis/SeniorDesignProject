from abc import ABC, abstractmethod
from dataclasses import dataclass, fields, is_dataclass
from typing import (
    Any,
    ClassVar,
    Generic,
    Protocol,
    TypeVar,
    TypeVarTuple,
    runtime_checkable,
)

from server.util.file.file import FileId
from server.util.file.manager import INetworkFileManager
from server.util.file.meta import MetaData

T = TypeVar("T")


@dataclass
class ObjectInfo:
    version: int


@dataclass
class LoadedObject(Generic[T]):
    id: FileId
    info: ObjectInfo
    data: T


@dataclass
class ObjectDescription:
    id: FileId
    info: ObjectInfo
    meta: MetaData


TData = TypeVar("TData")
Ts = TypeVarTuple("Ts")


class DataclassProtocol(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]


DEFAULT_FIELDS = {"meta", "data"}  # If this protocol changes, so must the default fields


class LoadableObjectProtocol(DataclassProtocol, Protocol, Generic[TData, *Ts]):
    meta: MetaData
    data: TData

    def __init__(self, meta: MetaData, data: TData, *args: *Ts) -> None: ...

    def extra(self) -> tuple[*Ts]: ...


@dataclass
class Loadable:

    def __post_init__(self):
        self.extra_fields = [field.name for field in fields(self) if field.name not in DEFAULT_FIELDS]

    def extra(self):
        return tuple(getattr(self, field) for field in self.extra_fields)
