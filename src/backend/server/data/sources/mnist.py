import os
from pathlib import Path
from typing import Any, Self, final, override
from torchvision.datasets import FashionMNIST

from server.data.sources.pytorch_base import DatasetSource
from server.data.sources.base import DS_ROOT, DataSourceDefinition
from server.params import BoolParameter


@final
class FashionMNISTSource(DatasetSource[FashionMNIST]):
    def setup(self) -> None:
        self.dataset.download()


mnist_labels = DataSourceDefinition(
    "fashion_mnist_labels",
    "Fashion MNIST Labels",
    (BoolParameter("train", "Use Training Data", True),),
    lambda train, **_: FashionMNISTSource(FashionMNIST(Path(DS_ROOT, "fashion_mnist"), train), True),
)

mnist_values = DataSourceDefinition(
    "fashion_mnist_values",
    "Fashion MNIST Values",
    (BoolParameter("train", "Use Training Data", True),),
    lambda train, **_: FashionMNISTSource(FashionMNIST(Path(DS_ROOT, "fashion_mnist"), train), False),
)
