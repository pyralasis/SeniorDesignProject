import torch
from server.layer import LayerDefinition
from server.layer.input import InputDefinition
from server.layer.size import size_identity
from server.params import BoolParameter, FloatParameter, IntParameter

# Found here: https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity

elu_layer = LayerDefinition(
    "elu",
    "ELU",
    (InputDefinition(None, 1, None),),
    (
        FloatParameter(id="alpha", name="Alpha", default=1.0),
        BoolParameter("inplace", "Inplace", False),
    ),
    lambda in_sizes, alpha, inplace, **_: torch.nn.ELU(alpha, inplace),
    lambda in_sizes, **_: in_sizes[0],
)

leakyrelu_layer = LayerDefinition(
    "leakyrelu",
    "LeakyReLU",
    (InputDefinition(None, 1, None),),
    (
        FloatParameter(id="negative_slope", name="Negative Slope", default=1.0),
        BoolParameter("inplace", "Inplace", False),
    ),
    lambda in_sizes, negative_slope, inplace, **_: torch.nn.LeakyReLU(negative_slope, inplace),
    lambda in_sizes, **_: in_sizes[0],
)

prelu_layer = LayerDefinition(
    "prelu",
    "PReLU",
    (InputDefinition(None, 1, None),),
    (
        IntParameter("num_parameters", "Num Parameters", 1),
        FloatParameter(id="alpha", name="Alpha", default=1.0),
    ),
    lambda in_sizes, num_parameters, alpha, **_: torch.nn.PReLU(num_parameters, alpha),
    lambda in_sizes, **_: in_sizes[0],
)

relu_layer = LayerDefinition(
    "relu",
    "ReLU",
    (InputDefinition(None, 1, None),),
    (BoolParameter("inplace", "Inplace", False),),
    lambda in_sizes, inplace, **_: torch.nn.ReLU(inplace),
    lambda in_sizes, **_: in_sizes[0],
)

logsigmoid_layer = LayerDefinition(
    "logsigmoid",
    "LogSigmoid",
    (InputDefinition(None, 1, None),),
    (),
    lambda in_sizes, **_: torch.nn.LogSigmoid(),
    lambda in_sizes, **_: in_sizes[0],
)

sigmoid_layer = LayerDefinition(
    "sigmoid",
    "Sigmoid",
    (InputDefinition(None, 1, None),),
    (),
    lambda in_sizes, **_: torch.nn.Sigmoid(),
    lambda in_sizes, **_: in_sizes[0],
)

tanh_layer = LayerDefinition(
    "tanh",
    "TanH",
    (InputDefinition(None, 1, None),),
    (),
    lambda in_sizes, **_: torch.nn.Tanh(),
    lambda in_sizes, **_: in_sizes[0],
)


# Found here: https://pytorch.org/docs/stable/nn.html#non-linear-activations-other

softmin_layer = LayerDefinition(
    "softmin",
    "Softmin",
    (InputDefinition(None, 1, None),),
    (IntParameter("dim", "Dim", 1),),
    lambda in_sizes, dim, **_: torch.nn.Softmin(dim),
    lambda in_sizes, **_: in_sizes[0],
)

softmax_layer = LayerDefinition(
    "softmax",
    "Softmax",
    (InputDefinition(None, 1, None),),
    (IntParameter("dim", "Dim", 1),),
    lambda in_sizes, dim, **_: torch.nn.Softmax(dim),
    lambda in_sizes, **_: in_sizes[0],
)
