from dataclasses import dataclass
from typing import Generic, TypeVar

from .id import FileId

T = TypeVar("T")


@dataclass
class Loaded(Generic[T]):
    id: FileId
    data: T
