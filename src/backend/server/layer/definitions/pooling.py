from math import ceil, floor
import torch
from server.layer import Layer
from server.layer.input import InputDefinition, InputType
from server.params import (
    BoolParameter,
    Size2DParameter,
)
from server.layer.size import TensorSize

# found here: https://pytorch.org/docs/stable/nn.html#convolution-layers


# TODO: Write tests for this?
def pool_2d_size_transformation(
    in_size: TensorSize,
    kernel_size: tuple[int, int],
    stride: tuple[int, int],
    padding: tuple[int, int],
    dilation: tuple[int, int],
    ceil_mode: bool,
    *_
) -> TensorSize:
    rounding_func = ceil if ceil_mode else floor

    h_in = in_size[-2]
    h_out = rounding_func(
        (h_in + 2 * padding[0] - dilation[0] * (kernel_size[0] - 1) - 1) / stride[0] + 1
    )

    w_in = in_size[-1]
    w_out = rounding_func(
        (w_in + 2 * padding[1] - dilation[1] * (kernel_size[1] - 1) - 1) / stride[1] + 1
    )
    return TensorSize(in_size[:-2] + (h_out, w_out))


max_pool2d_layer = Layer(
    "max_pool2d",
    "2D Max Pooling",
    InputDefinition(InputType.Single, 3, 4),
    (
        Size2DParameter("kernel_size", "Kernel", (3, 3)),
        Size2DParameter("stride", "Stride", (1, 1)),
        Size2DParameter("padding", "Padding", (0, 0)),
        Size2DParameter("dilation", "Dilation", (1, 1)),
        BoolParameter("ceil_mode", "Ceil Output Shape", False),
    ),
    lambda _in_size, kernel_size, stride, padding, dilation, ceil_mode: torch.nn.MaxPool2d(
        kernel_size,
        stride=stride,
        padding=padding,
        dilation=dilation,
        ceil_mode=ceil_mode,
    ),
    pool_2d_size_transformation,
)
