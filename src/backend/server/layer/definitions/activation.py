import torch
from server.layer import Layer
from server.layer.size import size_identity
from server.layer.input import InputDefinition, InputType

# Found here: https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity

relu_layer = Layer(
    "relu",
    InputDefinition(InputType.Single, 1, None),
    (),
    lambda: torch.nn.ReLU(),
    size_identity,
)
