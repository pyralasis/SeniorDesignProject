import torch
from server.layer import LayerDefinition
from server.layer.input import InputDefinition
from server.layer.size import size_identity

# Found here: https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity

relu_layer = LayerDefinition(
    "relu",
    "ReLU",
    (InputDefinition(None, 1, None),),
    (),
    lambda in_sizes, **_: torch.nn.ReLU(),
    lambda in_sizes, **_: in_sizes[0],
)
