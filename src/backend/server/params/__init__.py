__all__ = [
    "ParamType",
    "Parameter",
    "ParameterValue",
    "IntParameter",
    "IntParameterValue",
    "FloatParameter",
    "FloatParameterValue",
    "BoolParameter",
    "BoolParameterValue",
    "StringParameter",
    "StringParameterValue",
    "Size2D",
    "Size2DParameter",
    "Size2DParameterValue",
    "AnyParameter",
    "AnyParameterValue",
    "ParameterTuple",
    "ParameterValueTuple",
]

from dataclasses import KW_ONLY, dataclass
from enum import Enum
from typing import Generic, Literal, TypeAlias, TypeVar

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
    val: int
    type: Literal[ParamType.Int] = ParamType.Int


#
# Float
#


@dataclass
class FloatParameter(Parameter[float]):
    type: Literal[ParamType.Float] = ParamType.Float


@dataclass
class FloatParameterValue(ParameterValue[float]):
    val: float
    type: Literal[ParamType.Float] = ParamType.Float


#
# Bool
#


@dataclass
class BoolParameter(Parameter[bool]):
    type: Literal[ParamType.Bool] = ParamType.Bool


@dataclass
class BoolParameterValue(ParameterValue[bool]):
    val: bool
    type: Literal[ParamType.Bool] = ParamType.Bool


#
# String
#


@dataclass
class StringParameter(Parameter[str]):
    type: Literal[ParamType.String] = ParamType.String


@dataclass
class StringParameterValue(ParameterValue[str]):
    val: str
    type: Literal[ParamType.String] = ParamType.String


#
# Size
#

Size2D: TypeAlias = tuple[int, int]


@dataclass
class Size2DParameter(Parameter[Size2D]):
    type: Literal[ParamType.Size2D] = ParamType.Size2D


@dataclass
class Size2DParameterValue(ParameterValue[Size2D]):
    val: Size2D
    type: Literal[ParamType.Size2D] = ParamType.Size2D


#
# Any Parameter Type
#

AnyParameter = IntParameter | FloatParameter | BoolParameter | StringParameter | Size2DParameter
AnyParameterValue = (
    IntParameterValue | FloatParameterValue | BoolParameterValue | StringParameterValue | Size2DParameterValue
)

T0 = TypeVar("T0")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")
T8 = TypeVar("T8")
T9 = TypeVar("T9")

ParameterTuple: TypeAlias = (
    tuple[
        Parameter[T0],
        Parameter[T1],
        Parameter[T2],
        Parameter[T3],
        Parameter[T4],
        Parameter[T5],
        Parameter[T6],
        Parameter[T7],
        Parameter[T8],
        Parameter[T9],
    ]
    | tuple[
        Parameter[T0],
        Parameter[T1],
        Parameter[T2],
        Parameter[T3],
        Parameter[T4],
        Parameter[T5],
        Parameter[T6],
        Parameter[T7],
        Parameter[T8],
    ]
    | tuple[
        Parameter[T0],
        Parameter[T1],
        Parameter[T2],
        Parameter[T3],
        Parameter[T4],
        Parameter[T5],
        Parameter[T6],
        Parameter[T7],
    ]
    | tuple[
        Parameter[T0],
        Parameter[T1],
        Parameter[T2],
        Parameter[T3],
        Parameter[T4],
        Parameter[T5],
        Parameter[T6],
    ]
    | tuple[
        Parameter[T0],
        Parameter[T1],
        Parameter[T2],
        Parameter[T3],
        Parameter[T4],
        Parameter[T5],
    ]
    | tuple[Parameter[T0], Parameter[T1], Parameter[T2], Parameter[T3], Parameter[T4]]
    | tuple[Parameter[T0], Parameter[T1], Parameter[T2], Parameter[T3]]
    | tuple[Parameter[T0], Parameter[T1], Parameter[T2]]
    | tuple[Parameter[T0], Parameter[T1]]
    | tuple[Parameter[T0]]
    | tuple[()]
)

ParameterValueTuple: TypeAlias = (
    tuple[
        T0,
        T1,
        T2,
        T3,
        T4,
        T5,
        T6,
        T7,
        T8,
        T9,
    ]
    | tuple[
        T0,
        T1,
        T2,
        T3,
        T4,
        T5,
        T6,
        T7,
        T8,
    ]
    | tuple[
        T0,
        T1,
        T2,
        T3,
        T4,
        T5,
        T6,
        T7,
    ]
    | tuple[
        T0,
        T1,
        T2,
        T3,
        T4,
        T5,
        T6,
    ]
    | tuple[
        T0,
        T1,
        T2,
        T3,
        T4,
        T5,
    ]
    | tuple[T0, T1, T2, T3, T4]
    | tuple[T0, T1, T2, T3]
    | tuple[T0, T1, T2]
    | tuple[T0, T1]
    | tuple[T0]
    | tuple[()]
)
