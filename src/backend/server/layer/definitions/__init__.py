__all__ = ["default_layers"]

from . import activation, convolution, linear, pooling

default_layers = [
    activation.elu_layer,
    activation.relu_layer,
    activation.sigmoid_layer,
    activation.softmin_layer,
    activation.softmax_layer,
    convolution.conv2d_layer,
    convolution.fold_layer,
    convolution.unfold_layer,
    linear.linear_layer,
    # linear.bilinear_layer,
    pooling.max_pool2d_layer,
]
