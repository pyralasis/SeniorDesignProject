import torch
from server.params import BoolParameter, FloatParameter, IntParameter
from server.layer import LayerDefinition
from server.layer.input import InputDefinition
from server.layer.size import size_identity

# Found here: https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity

# elu_layer = LayerDefinition(
#     "elu",
#     "ELU",
#     (InputDefinition(None, 1, None),),
#     (
#         FloatParameter("alpha", "Alpha", 1.0),
#         BoolParameter("inplace", "Inplace", False)
#     ),
#     lambda in_sizes, alpha, inplace, **_: torch.nn.ELU(alpha, inplace),
#     lambda in_sizes, **_: in_sizes[0],
# )

relu_layer = LayerDefinition(
    "relu",
    "ReLU",
    (InputDefinition(None, 1, None),),
    (
        BoolParameter("inplace", "Inplace", False)
    ),
    lambda in_sizes, inplace, **_: torch.nn.ReLU(),
    lambda in_sizes, **_: in_sizes[0],
)

# sigmoid_layer = LayerDefinition(
#     "sigmoid",
#     "Sigmoid",
#     (InputDefinition(None, 1, None),),
#     (),
#     lambda in_sizes, **_: torch.nn.Sigmoid(),
#     lambda in_sizes, **_: in_sizes[0],
# )

# Found here: https://pytorch.org/docs/stable/nn.html#non-linear-activations-other

# softmin_layer = LayerDefinition(
#     "softmin",
#     "Softmin",
#     (InputDefinition(None, 1, None),),
#     (
#         IntParameter("dim", "Dim", 1)
#     ),
#     lambda in_sizes, dim, **_: torch.nn.Softmin(dim),
#     lambda in_sizes, **_: in_sizes[0],
# )

# softmax_layer = LayerDefinition(
#     "softmax",
#     "Softmax",
#     (InputDefinition(None, 1, None),),
#     (
#         IntParameter("dim", "Dim", 1)
#     ),
#     lambda in_sizes, dim, **_: torch.nn.Softmax(dim),
#     lambda in_sizes, **_: in_sizes[0],
# )