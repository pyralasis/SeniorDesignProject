from dataclasses import dataclass
from typing import Generic, TypeAlias, TypeVar

T = TypeVar("T")

FileId: TypeAlias = int


def is_file_id(val: str) -> bool:
    return val.isdigit()


@dataclass
class LoadedFile(Generic[T]):
    id: FileId
    data: T
