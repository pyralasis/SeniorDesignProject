__all__ = ["default_layers"]

from . import activation
from . import convolution
from . import linear
from . import pooling

default_layers = [
    activation.relu_layer,
    
    convolution.conv2d_layer,

    linear.linear_layer,
    linear.bilinear_layer,

    pooling.max_pool2d_layer
]