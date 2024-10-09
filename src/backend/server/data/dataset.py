from dataclasses import dataclass
from typing import TypeAlias


DatasetID: TypeAlias = str


@dataclass
class Dataset:
    id: DatasetID
    name: str
