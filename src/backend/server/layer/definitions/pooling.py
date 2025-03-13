from math import ceil, floor
import torch
from server.layer import LayerDefinition
from server.layer.input import InputDefinition
from server.params import (
    BoolParameter,
    Size2DParameter,
)
from server.layer.size import TensorSize

# found here: https://pytorch.org/docs/stable/nn.html#pooling-layers


# TODO: Write tests for this?
def pool_2d_size_transformation(
    in_sizes: tuple[TensorSize, ...],
    kernel_size: tuple[int, int],
    stride: tuple[int, int],
    padding: tuple[int, int],
    dilation: tuple[int, int],
    ceil_mode: bool,
    **_
) -> TensorSize:
    in_size = in_sizes[0]
    rounding_func = ceil if ceil_mode else floor

    h_in = in_size[-2]
    h_out = rounding_func((h_in + 2 * padding[0] - dilation[0] * (kernel_size[0] - 1) - 1) / stride[0] + 1)

    w_in = in_size[-1]
    w_out = rounding_func((w_in + 2 * padding[1] - dilation[1] * (kernel_size[1] - 1) - 1) / stride[1] + 1)
    return TensorSize(in_size[:-2] + (h_out, w_out))


max_pool2d_layer = LayerDefinition(
    "max_pool2d",
    "2D Max Pooling",
    (InputDefinition(None, 3, 4),),
    (
        Size2DParameter("kernel_size", "Kernel", (3, 3)),
        Size2DParameter("stride", "Stride", (1, 1)),
        Size2DParameter("padding", "Padding", (0, 0)),
        Size2DParameter("dilation", "Dilation", (1, 1)),
        BoolParameter("ceil_mode", "Ceil Output Shape", False),
    ),
    lambda in_sizes, kernel_size, stride, padding, dilation, ceil_mode, **_: (
        torch.nn.MaxPool2d(
            kernel_size,
            stride=stride,
            padding=padding,
            dilation=dilation,
            ceil_mode=ceil_mode,
        )
    ),
    pool_2d_size_transformation,
)

def avg_pool_2d_size_transformation(
    in_sizes: tuple[TensorSize, ...],
    kernel_size: tuple[int, int],
    stride: tuple[int, int],
    padding: tuple[int, int],
    ceil_mode: bool,
    **_
) -> TensorSize:
    in_size = in_sizes[0]
    rounding_func = ceil if ceil_mode else floor

    h_in = in_size[-2]
    h_out = rounding_func((h_in + 2 * padding[0] - kernel_size[0] ) / stride[0] + 1)

    w_in = in_size[-1]
    w_out = rounding_func((w_in + 2 * padding[1] - kernel_size[1]) / stride[1] + 1)
    return TensorSize(in_size[:-2] + (h_out, w_out))


avgpool2d_layer = LayerDefinition(
    "avgpool2d",
    "Avg Pool 2D",
    (InputDefinition(None, 3, 4),),
    (
        Size2DParameter("kernel_size", "Kernel", (3, 3)),
        Size2DParameter("stride", "Stride", (1, 1)),
        Size2DParameter("padding", "Padding", (0, 0)),
        BoolParameter("ceil_mode", "Ceil Output Shape", False),
        BoolParameter("count_include_pad", "Count Include Pade", False),
        # TODO: DIVISOR OVERRIDE ASK GARETH
    ),
    lambda in_sizes, kernel_size, stride, padding, ceil_mode, count_include_pad, **_: (
        torch.nn.AvgPool2d(
            kernel_size,
            stride=stride,
            padding=padding,
            ceil_mode=ceil_mode,
            count_include_pad=count_include_pad,
        )
    ),
    avg_pool_2d_size_transformation,
)

def l_pool_2d_size_transformation(
    in_sizes: tuple[TensorSize, ...],
    kernel_size: tuple[int, int],
    stride: tuple[int, int],
    padding: tuple[int, int],
    ceil_mode: bool,
    **_
) -> TensorSize:
    in_size = in_sizes[0]
    rounding_func = ceil if ceil_mode else floor

    h_in = in_size[-2]
    h_out = rounding_func((h_in - kernel_size[0] ) / stride[0] + 1)

    w_in = in_size[-1]
    w_out = rounding_func((w_in - kernel_size[1]) / stride[1] + 1)
    return TensorSize(in_size[:-2] + (h_out, w_out))


lpool2d_layer = LayerDefinition(
    "lpool2d",
    "L Pool 2D",
    (InputDefinition(None, 3, 4),),
    (
        Size2DParameter("kernel_size", "Kernel", (3, 3)),
        Size2DParameter("stride", "Stride", (1, 1)),
        BoolParameter("ceil_mode", "Ceil Output Shape", False),
    ),
    lambda in_sizes, kernel_size, stride, ceil_mode, **_: (
        torch.nn.AvgPool2d(
            kernel_size,
            stride=stride,
            ceil_mode=ceil_mode,
        )
    ),
    l_pool_2d_size_transformation,
)