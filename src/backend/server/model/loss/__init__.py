__all__ = ["default_loss_fns"]

from . import basic

default_loss_fns = [basic.nll_loss, basic.mse_loss, basic.cross_entropy_loss]
