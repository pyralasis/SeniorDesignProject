from typing import NewType


TensorSize = NewType("TensorSize", tuple[int, ...])


def size_identity(in_size: TensorSize, *_) -> TensorSize:
    return in_size
