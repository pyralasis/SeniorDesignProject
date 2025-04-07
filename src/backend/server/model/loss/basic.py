import torch
from server.model.loss.definition import LossDefinition
from server.params import FloatParameter

# NLL Loss
nll_loss = LossDefinition(
    "nll_loss",
    "Negative Log Likelihood Loss",
    (),
    lambda **params: torch.nn.NLLLoss(**params, reduction="sum"),
)

# Cross Entropy
cross_entropy_loss = LossDefinition(
    "cross_entropy",
    "Cross Entropy Loss",
    (),
    lambda **params: torch.nn.CrossEntropyLoss(**params),
)

# Mean Squared Error
mse_loss = LossDefinition(
    "mse_loss",
    "Mean Squared Error Loss",
    (),
    lambda **params: torch.nn.MSELoss(**params),
)
