from typing import NewType, TypeAlias

TensorSize = NewType("TensorSize", tuple[int, ...])


def size_identity(in_sizes: tuple[TensorSize, ...], *_) -> TensorSize:
    return in_sizes[0]
