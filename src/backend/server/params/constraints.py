from abc import ABC
from dataclasses import KW_ONLY, dataclass
from typing import Generic, Literal, TypeVar

T = TypeVar("T")


@dataclass
class ParameterConstraint(ABC, Generic[T]):
    _: KW_ONLY
    type: str


@dataclass
class OneOf(Generic[T], ParameterConstraint[T]):
    values: list[T]
    _: KW_ONLY
    type: Literal["oneof"] = "oneof"


@dataclass
class WithRange(ParameterConstraint[int]):
    min: int | None = None
    max: int | None = None
    _: KW_ONLY
    type: Literal["range"] = "range"
