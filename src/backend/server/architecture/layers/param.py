from dataclasses import KW_ONLY, dataclass
from enum import Enum
from typing import Any, Generic, Literal, TypeVar

T = TypeVar("T")

class ParamMeta(type):
    def __new__(cls, name: str, bases: tuple[type, ...], dict: dict[str, Any]):
        return super().__new__(cls, name, bases[:-1], dict)



#
# Base
#

class ParamType(str, Enum):
    Int = "int"
    Float = "float"
    Bool = "bool"

@dataclass
class Parameter(Generic[T]):
    name: str
    default: T
    _: KW_ONLY
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
class IntParameter(Parameter[int], int, metaclass=ParamMeta):
    type: Literal[ParamType.Int] = ParamType.Int

@dataclass
class IntParameterValue(ParameterValue[int]):
    type: Literal[ParamType.Int] = ParamType.Int

#
# Float
#

@dataclass
class FloatParameter(Parameter[float], float, metaclass=ParamMeta):
    type: Literal[ParamType.Float] = ParamType.Float

@dataclass
class FloatParameterValue(ParameterValue[float]):
    type: Literal[ParamType.Float] = ParamType.Float

#
# Bool
#

@dataclass
class BoolParameter(Parameter[bool], bool, metaclass=ParamMeta): # type: ignore
    type: Literal[ParamType.Bool] = ParamType.Bool

@dataclass
class BoolParameterValue(ParameterValue[bool]):
    type: Literal[ParamType.Bool] = ParamType.Bool

#
# Any Parameter Type
#

LayerParameter = IntParameter | FloatParameter | BoolParameter
