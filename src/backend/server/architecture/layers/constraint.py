from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

class ParameterConstraint(ABC, Generic[T]):
    ...

@dataclass
class OneOf(Generic[T], ParameterConstraint[T]):
    values: list[T]

@dataclass
class WithRange(ParameterConstraint[int]):
    min: int | None = None
    max: int | None = None
