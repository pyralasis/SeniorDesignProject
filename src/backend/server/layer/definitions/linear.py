import torch
from server.layer import Layer
from server.layer.constraint import WithRange
from server.layer.input import InputDefinition, InputType
from server.layer.param import BoolParameter, IntParameter
from server.layer.size import TensorSize

# found here: https://pytorch.org/docs/stable/nn.html#linear-layers


def linear_size_transformation(
    in_size: TensorSize, output_features: int, *_
) -> TensorSize:
    return TensorSize(in_size[:-1] + (output_features,))


linear_layer = Layer(
    "linear",
    InputDefinition(InputType.Single, 1, None),
    (
        IntParameter("out_features", "Output Features", 1, constraint=WithRange(1)),
        BoolParameter("bias", "Bias", True),
    ),
    lambda size, out_features, bias: torch.nn.Linear(size[-1], out_features, bias),
    linear_size_transformation,
)
