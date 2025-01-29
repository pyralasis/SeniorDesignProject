from pathlib import Path
from typing import final
from torchvision.datasets import MNIST

from server.data.sources.pytorch_base import TorchDatasetSource
from server.data.sources.base import DS_ROOT, DataSourceDefinition
from server.params import BoolParameter

@final
class MNISTSource(TorchDatasetSource[MNIST]):
    def setup(self) -> None:
        self.dataset.download()


mnist_labels = DataSourceDefinition(
    "mnist_labels",
    "MNIST Labels",
    (BoolParameter("train", "Use Training Data", True),),
    lambda train, **_: MNISTSource(MNIST(Path(DS_ROOT, "mnist"), train), True),
)

mnist_values = DataSourceDefinition(
    "mnist_values",
    "MNIST Values",
    (BoolParameter("train", "Use Training Data", True),),
    lambda train, **_: MNISTSource(MNIST(Path(DS_ROOT, "mnist"), train), False),
)
