from math import floor

import torch
from server.layer import LayerDefinition
from server.layer.input import InputDefinition
from server.layer.size import TensorSize, size_identity
from server.params import BoolParameter, IntParameter, Size2DParameter, StringParameter
from server.params.constraints import OneOf, WithRange

# found here: https://pytorch.org/docs/stable/nn.html#convolution-layers


# TODO: Write tests for this?
def conv_2d_size_transformation(
    in_sizes: tuple[TensorSize, ...],
    out_channels: int,
    kernel_size: tuple[int, int],
    stride: tuple[int, int],
    padding: tuple[int, int],
    dilation: tuple[int, int],
    **_
) -> TensorSize:
    in_size = in_sizes[0]

    h_in = in_size[-2]
    h_out = floor((h_in + 2 * padding[0] - dilation[0] * (kernel_size[0] - 1) - 1) / stride[0] + 1)

    w_in = in_size[-1]
    w_out = floor((w_in + 2 * padding[1] - dilation[1] * (kernel_size[1] - 1) - 1) / stride[1] + 1)
    return TensorSize(in_size[:-3] + (out_channels, h_out, w_out))


conv2d_layer = LayerDefinition(
    "conv2d",
    "2D Convolution",
    (InputDefinition(None, 3, 4),),
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
    lambda in_sizes, out_channels, kernel_size, stride, padding, padding_mode, dilation, groups, bias, **_: (
        torch.nn.Conv2d(
            in_sizes[0][-3],
            out_channels,
            kernel_size,
            stride=stride,
            padding=padding,
            padding_mode=padding_mode,
            dilation=dilation,
            groups=groups,
            bias=bias,
        )
    ),
    conv_2d_size_transformation,
)
