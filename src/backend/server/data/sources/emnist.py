from pathlib import Path
from typing import final

from server.data.sources.base import DS_ROOT, DataSourceDefinition
from server.data.sources.pytorch_base import TorchDatasetSource
from server.params import BoolParameter
from torchvision.datasets import EMNIST


@final
class EMNISTSource(TorchDatasetSource[EMNIST]): ...


emnist_labels = DataSourceDefinition(
    "emnist_labels",
    "EMNIST Labels",
    (BoolParameter("train", "Use Training Data", True),),
    lambda train, **_: EMNISTSource(EMNIST(Path(DS_ROOT, "emnist"), train, download=True), True),
)

emnist_values = DataSourceDefinition(
    "emnist_values",
    "EMNIST Values",
    (BoolParameter("train", "Use Training Data", True),),
    lambda train, **_: EMNISTSource(EMNIST(Path(DS_ROOT, "emnist"), train, download=True), False),
)
