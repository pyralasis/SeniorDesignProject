from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass
class Loaded(Generic[T]):
    file_name: str
    data: T
