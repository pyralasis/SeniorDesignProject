from dataclasses import KW_ONLY, dataclass
from enum import Enum
from typing import Generic, Literal, TypeVar

from server.params.constraints import ParameterConstraint


T = TypeVar("T")

# class ParamMeta(type):
#     def __new__(cls, name: str, bases: tuple[type, ...], dict: dict[str, Any]):
#         return super().__new__(cls, name, bases[:-1], dict)


#
# Base
#


class ParamType(str, Enum):
    Int = "int"
    Float = "float"
    Bool = "bool"
    String = "str"
    Size2D = "size2d"


@dataclass
class Parameter(Generic[T]):
    id: str
    name: str
    default: T
    _: KW_ONLY
    constraint: ParameterConstraint[T] | None = None
    type: ParamType


@dataclass
class ParameterValue(Generic[T]):
    val: T
    _: KW_ONLY
    type: ParamType


#
# Integer
#


@dataclass
class IntParameter(Parameter[int]):
    type: Literal[ParamType.Int] = ParamType.Int


@dataclass
class IntParameterValue(ParameterValue[int]):
    type: Literal[ParamType.Int] = ParamType.Int


#
# Float
#


@dataclass
class FloatParameter(Parameter[float], float):
    type: Literal[ParamType.Float] = ParamType.Float


@dataclass
class FloatParameterValue(ParameterValue[float]):
    type: Literal[ParamType.Float] = ParamType.Float


#
# Bool
#


@dataclass
class BoolParameter(Parameter[bool]):
    type: Literal[ParamType.Bool] = ParamType.Bool


@dataclass
class BoolParameterValue(ParameterValue[bool]):
    type: Literal[ParamType.Bool] = ParamType.Bool


#
# String
#


@dataclass
class StringParameter(Parameter[str]):
    type: Literal[ParamType.String] = ParamType.String


@dataclass
class StringParameterValue(ParameterValue[str]):
    type: Literal[ParamType.String] = ParamType.String


#
# Size
#


@dataclass
class Size2DParameter(Parameter[tuple[int, int]]):
    type: Literal[ParamType.Size2D] = ParamType.Size2D


@dataclass
class Size2DParameterValue(ParameterValue[tuple[int, int]]):
    type: Literal[ParamType.Size2D] = ParamType.Size2D


#
# Any Parameter Type
#

AnyParameterValue = (
    IntParameterValue
    | FloatParameterValue
    | BoolParameterValue
    | StringParameterValue
    | Size2DParameterValue
)
LayerParameter = (
    IntParameter | FloatParameter | BoolParameter | StringParameter | Size2DParameter
)
