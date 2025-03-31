import torch
from server.model.optim.definition import OptimizerDefinition
from server.params import BoolParameter, FloatParameter, IntParameter
from server.params.constraints import WithRange, WithRangeFloat

adam_optim = OptimizerDefinition(
    "adam",
    "Adam",
    (
        FloatParameter("lr", "Learning Rate", 0.01, constraint=WithRangeFloat(0)),
        FloatParameter("beta_1", "Beta 1", 0.9, constraint=WithRangeFloat(0)),
        FloatParameter("beta_2", "Beta 2", 0.999, constraint=WithRangeFloat(0)),
        FloatParameter("eps", "Epsilon", 1e-08, constraint=WithRangeFloat(0)),
        FloatParameter("weight_decay", "Weight Decay", 0.0, constraint=WithRangeFloat(0)),
        BoolParameter("amsgrad", "AMSGrad", False),
    ),
    lambda model, lr, beta_1, beta_2, eps, weight_decay, amsgrad, **_: (
        torch.optim.Adam(
            model.parameters(),
            lr=lr,
            betas=(beta_1, beta_2),
            eps=eps,
            weight_decay=weight_decay,
            amsgrad=amsgrad,
        )
    ),
)
