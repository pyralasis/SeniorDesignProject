__all__ = ["default_layers"]

from . import activation
from . import convulution
from . import linear
from . import pooling

default_layers = [
    activation.relu_layer,
    convulution.conv2d_layer,
    linear.linear_layer,
    pooling.max_pool2d_layer
]