from pathlib import Path
from typing import final

from server.data.sources.base import DS_ROOT, DataSourceDefinition
from server.data.sources.pytorch_base import TorchDatasetSource
from server.params import BoolParameter
from torchvision.datasets import FashionMNIST


@final
class FashionMNISTSource(TorchDatasetSource[FashionMNIST]): ...


fashion_mnist_labels = DataSourceDefinition(
    "fashion_mnist_labels",
    "Fashion MNIST Labels",
    (BoolParameter("train", "Use Training Data", True),),
    lambda train, **_: FashionMNISTSource(FashionMNIST(Path(DS_ROOT, "fashion_mnist"), train, download=True), True),
)

fashion_mnist_values = DataSourceDefinition(
    "fashion_mnist_values",
    "Fashion MNIST Values",
    (BoolParameter("train", "Use Training Data", True),),
    lambda train, **_: FashionMNISTSource(FashionMNIST(Path(DS_ROOT, "fashion_mnist"), train, download=True), False),
)
