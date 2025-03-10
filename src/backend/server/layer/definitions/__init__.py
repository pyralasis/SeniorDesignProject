__all__ = ["default_layers"]

from . import activation, convolution, dropout, linear, pooling

default_layers = [
    activation.elu_layer,
    activation.leakyrelu_layer,
    activation.prelu_layer,
    activation.relu_layer,
    activation.logsigmoid_layer,
    activation.sigmoid_layer,
    activation.tanh_layer,
    activation.softmin_layer,
    activation.softmax_layer,

    convolution.conv2d_layer,
    convolution.fold_layer,
    convolution.unfold_layer,

    dropout.dropout_layer,

    linear.linear_layer,
    # linear.bilinear_layer,

    pooling.max_pool2d_layer,
    pooling.avgpool2d_layer,
    pooling.lpool2d_layer,
]
