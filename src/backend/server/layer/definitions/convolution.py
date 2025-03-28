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
    return (out_channels, h_out, w_out)


conv2d_layer = LayerDefinition(
    "conv2d",
    "2D Convolution",
    (InputDefinition(None, 3, 3),),
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
            in_sizes[0][0],
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


def fold_size_transformation(
    input_dims: tuple[TensorSize, ...], output_size: tuple[int, int], kernel_size: int, **_
) -> TensorSize:
    input_dim = input_dims[0]

    num_spatial_dims = len(input_dim) - 2
    kernel_count: int = kernel_size**num_spatial_dims

    if len(input_dim) == 2:
        C = input_dim[0] // kernel_count
        return (C, output_size[0], output_size[1])
    else:
        C = input_dim[1] // kernel_count
        return (input_dim[0], C, output_size[0], output_size[1])


fold_layer = LayerDefinition(
    "fold",
    "Fold",
    (InputDefinition(None, 2, 3),),
    # TODO: These parameters can be ints or tuples. Leaving as just Ints for now
    # See https://pytorch.org/docs/stable/generated/torch.nn.Fold.html#torch.nn.Fold
    (
        Size2DParameter("output_size", "Output Size", (5, 5)),  # Really should fix this one at least
        IntParameter("kernel_size", "Kernel", 5),
        IntParameter("dilation", "Dilation", 1),
        IntParameter("padding", "Padding", 0),
        IntParameter("stride", "Stride", 1),
    ),
    lambda in_sizes, kernel_size, dilation, padding, stride, **_: (
        torch.nn.Fold(in_sizes[0], kernel_size, dilation, padding, stride)
    ),
    fold_size_transformation,
)


def unfold_size_transformation(d: tuple[TensorSize, ...], padding, dilation, kernel_size, stride, **_):
    size = d[0]

    L = 1
    for i in range(2, len(size)):
        L *= floor(((size[i] + 2 * padding - dilation * (kernel_size - 1) - 1) / stride) + 1)

    num_spatial_dims = len(size) - 2
    return (size[0], size[1] * kernel_size**num_spatial_dims, L)  # Size tuple


unfold_layer = LayerDefinition(
    "unfold",
    "Unfold",
    (InputDefinition(None, 2, None),),
    # TODO: These parameters can be ints or tuples. Leaving as just Ints for now
    # See https://pytorch.org/docs/stable/generated/torch.nn.Unfold.html#torch.nn.Unfold
    (
        IntParameter("kernel_size", "Kernel", 5),
        IntParameter("dilation", "Dilation", 1),
        IntParameter("padding", "Padding", 0),
        IntParameter("stride", "Stride", 1),
    ),
    lambda kernel_size, dilation, padding, stride, **_: (torch.nn.Unfold(kernel_size, dilation, padding, stride)),
    unfold_size_transformation,
)
