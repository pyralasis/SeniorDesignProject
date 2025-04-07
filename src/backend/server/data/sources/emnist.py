from pathlib import Path
from typing import final

from server.data.sources.base import DS_ROOT, DataSourceDefinition
from server.data.sources.pytorch_base import TorchDatasetSource
from server.params import BoolParameter, StringParameter
from torchvision.datasets import EMNIST


@final
class EMNISTSource(TorchDatasetSource[EMNIST]): ...


emnist_labels = DataSourceDefinition(
    "emnist_labels",
    "EMNIST Labels",
    (StringParameter("split", "Split", ""), BoolParameter("train", "Use Training Data", True),),
    lambda split, train, **_: EMNISTSource(EMNIST(Path(DS_ROOT, "emnist"), split, train=train, download=True), True),
)

emnist_values = DataSourceDefinition(
    "emnist_values",
    "EMNIST Values",
    (StringParameter("split", "Split", ""), BoolParameter("train", "Use Training Data", True),),
    lambda split, train, **_: EMNISTSource(EMNIST(Path(DS_ROOT, "emnist"), split, train=train, download=True), False),
)
