from dataclasses import dataclass
from typing import TypeAlias


TransformID: TypeAlias = str


@dataclass
class Transform:
    id: TransformID
    name: str
