from math import floor
import torch
from server.architecture.layers import Layer
from server.architecture.layers.constraint import OneOf, WithRange
from server.architecture.layers.input import InputDefinition, InputType
from server.architecture.layers.param import (
    BoolParameter,
    IntParameter,
    Size2DParameter,
    StringParameter,
)
from server.architecture.layers.size import TensorSize, size_identity

# found here: https://pytorch.org/docs/stable/nn.html#convolution-layers


# TODO: Write tests for this?
def conv_2d_size_transformation(
    in_size: TensorSize,
    out_channels: int,
    kernel_size: tuple[int, int],
    stride: tuple[int, int],
    padding: tuple[int, int],
    _padding_mode: str,
    dilation: tuple[int, int],
) -> TensorSize:
    h_in = in_size[-2]
    h_out = floor(
        (h_in + 2 * padding[0] - dilation[0] * (kernel_size[0] - 1) - 1) / stride[0] + 1
    )

    w_in = in_size[-1]
    w_out = floor(
        (w_in + 2 * padding[1] - dilation[1] * (kernel_size[1] - 1) - 1) / stride[1] + 1
    )
    return TensorSize(in_size[:-3] + (out_channels, h_out, w_out))


conv2d_layer = Layer(
    "conv2d",
    InputDefinition(InputType.Single, 3, 4),
    (
        IntParameter("out_channels", "Output Channels", 1),
        Size2DParameter("kernel_size", "Kernel", (3, 3)),
        Size2DParameter("stride", "Stride", (1, 1)),
        Size2DParameter("padding", "Padding", (0, 0)),
        StringParameter(
            "padding_mode",
            "Padding Mode",
            "zeros",
            constraint=OneOf(["zeros", "reflect", "replicate", "circular"]),
        ),
        Size2DParameter("dilation", "Dilation", (1, 1)),
        IntParameter("groups", "Groups", 1, constraint=WithRange(1)),
        BoolParameter("bias", "Bias", True),
    ),
    lambda in_size, out_channels, kernel_size, stride, padding, padding_mode, dilation, groups, bias: torch.nn.Conv2d(
        in_size[-3],
        out_channels,
        kernel_size,
        stride=stride,
        padding=padding,
        padding_mode=padding_mode,
        dilation=dilation,
        groups=groups,
        bias=bias,
    ),
    conv_2d_size_transformation,
)
