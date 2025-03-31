import torch
from server.model.optim.definition import OptimizerDefinition
from server.params import BoolParameter, FloatParameter, IntParameter
from server.params.constraints import WithRange, WithRangeFloat

sgd_optim = OptimizerDefinition(
    "sgd",
    "SGD",
    (
        FloatParameter("lr", "Learning Rate", 0.01, constraint=WithRangeFloat(0)),
        FloatParameter("momentum", "Momentum", 0.0, constraint=WithRangeFloat(0)),
        FloatParameter("dampening", "Dampening", 0.0, constraint=WithRangeFloat(0)),
        FloatParameter("weight_decay", "Weight Decay", 0.0, constraint=WithRangeFloat(0)),
        BoolParameter("nesterov", "Nesterov", False),
    ),
    lambda model, lr, momentum, dampening, weight_decay, nesterov, **_: (
        torch.optim.SGD(model.parameters(), lr, momentum, dampening, weight_decay, nesterov)
    ),
)
