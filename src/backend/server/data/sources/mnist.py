from pathlib import Path
from typing import final, override

from server.data.sources.base import DS_ROOT, DataSourceDefinition
from server.data.sources.pytorch_base import TorchDatasetSource
from server.params import BoolParameter
from torchvision.datasets import MNIST


@final
class MNISTSource(TorchDatasetSource[MNIST]): ...


mnist_labels = DataSourceDefinition(
    "mnist_labels",
    "MNIST Labels",
    (BoolParameter("train", "Use Training Data", True),),
    lambda train, **_: MNISTSource(MNIST(Path(DS_ROOT, "mnist"), train, download=True), True),
)

mnist_values = DataSourceDefinition(
    "mnist_values",
    "MNIST Values",
    (BoolParameter("train", "Use Training Data", True),),
    lambda train, **_: MNISTSource(MNIST(Path(DS_ROOT, "mnist"), train, download=True), False),
)
