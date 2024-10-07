from dataclasses import dataclass
from enum import Enum


class InputType(str, Enum):
    Single = "single"
    Multiple = "multiple"


@dataclass
class InputDefinition:
    type: InputType
    min_dimensions: int
    max_dimensions: int | None
