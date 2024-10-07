import torch
from backend.server.architecture.layers import Layer
from backend.server.architecture.layers.size import size_identity
from server.architecture.layers.input import InputDefinition, InputType

# Found here: https://pytorch.org/docs/stable/nn.html#non-linear-activations-weighted-sum-nonlinearity

relu_layer = Layer(
    "relu",
    InputDefinition(InputType.Single, 1, None),
    (),
    lambda: torch.nn.ReLU(),
    size_identity,
)
