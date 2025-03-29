import torch
from server.layer import LayerDefinition
from server.layer.input import InputDefinition
from server.layer.size import TensorSize
from server.params import IntParameter


def flatten_size_transformation(
    in_sizes: tuple[TensorSize, ...],
    start_dim: int,
    end_dim: int,
    **_,
) -> TensorSize:
    in_size = in_sizes[0]

    if end_dim < 0:
        end_dim += len(in_size)

    flattened_size = 1
    for size in in_size[start_dim : end_dim + 1]:
        flattened_size *= size

    # Calculate the new size
    new_size = in_size[:start_dim] + (flattened_size,) + in_size[end_dim + 1 :]
    return TensorSize(new_size)


flatten_layer = LayerDefinition(
    "flatten",
    "Flatten",
    (InputDefinition(None, 1, None),),
    (
        IntParameter("start_dim", "Starting Dimension", 0),
        IntParameter("end_dim", "Ending Dimension", -1),
    ),
    lambda in_sizes, start_dim, end_dim, **_: torch.nn.Flatten(start_dim + 1, end_dim if end_dim < 0 else end_dim + 1),
    flatten_size_transformation,
)
