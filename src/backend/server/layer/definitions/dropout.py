from math import floor

import torch
from server.layer import LayerDefinition
from server.layer.input import InputDefinition
from server.layer.size import TensorSize, size_identity
from server.params import (
    BoolParameter,
    FloatParameter,
    IntParameter,
    Size2DParameter,
    StringParameter,
)
from server.params.constraints import OneOf, WithRangeFloat

# found here: https://pytorch.org/docs/stable/nn.html#dropout-layers

dropout_layer = LayerDefinition(
    "droput",
    "Dropout",
    (InputDefinition(None, 1, None),),
    (
        FloatParameter("p", "Dropout Probability", 0.5, constraint=WithRangeFloat(0, 1)),
        BoolParameter("inplace", "Inplace", False),
    ),
    lambda in_sizes, p, inplace, **_: torch.nn.Dropout(p, inplace),
    lambda in_sizes, **_: in_sizes[0],
)
