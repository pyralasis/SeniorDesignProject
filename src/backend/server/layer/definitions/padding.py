import torch
from server.layer import LayerDefinition
from server.layer.input import InputDefinition
from server.layer.size import TensorSize
from server.params import BoolParameter, FloatParameter, IntParameter
from server.params.constraints import WithRange

# found here: https://pytorch.org/docs/stable/nn.html#padding-layers

# TODO: PADDING CAN BE INT OR TUPLE GARETH WHAT DO AAAAAA


def constant_padding_1d_size_transformation(in_sizes: tuple[TensorSize, ...], padding: int, **_) -> TensorSize:
    in_size = in_sizes[0]
    w_out = in_size[-1] + padding * 2
    return TensorSize(in_size[:-1] + (w_out,))


constantpadding1d_layer = LayerDefinition(
    "constantpadding1d",
    "Constant Padding 1D",
    (InputDefinition(None, 2, 2),),
    (
        IntParameter("padding", "Padding", 0),
        FloatParameter("value", "Value", 0),
    ),
    lambda in_sizes, padding, value, **_: torch.nn.ConstantPad1d(padding, value),
    constant_padding_1d_size_transformation,
)


def constant_padding_2d_size_transformation(in_sizes: tuple[TensorSize, ...], padding: int, **_) -> TensorSize:
    in_size = in_sizes[0]

    h_out = in_size[1] + padding * 2
    w_out = in_size[2] + padding * 2
    return TensorSize((in_size[0], h_out, w_out))


constantpadding2d_layer = LayerDefinition(
    "constantpadding2d",
    "Constant Padding 2D",
    (InputDefinition(None, 3, 3),),
    (
        IntParameter("padding", "Padding", 0),
        FloatParameter("value", "Value", 0),
    ),
    lambda in_sizes, padding, value, **_: torch.nn.ConstantPad2d(padding, value),
    constant_padding_2d_size_transformation,
)


def constant_padding_3d_size_transformation(in_sizes: tuple[TensorSize, ...], padding: int, **_) -> TensorSize:
    in_size = in_sizes[0]

    d_out = in_size[1] + padding * 2
    h_out = in_size[2] + padding * 2
    w_out = in_size[3] + padding * 2
    return TensorSize((in_size[0], d_out, h_out, w_out))


constantpadding3d_layer = LayerDefinition(
    "constantpadding3d",
    "Constant Padding 3D",
    (InputDefinition(None, 4, 4),),
    (
        IntParameter("padding", "Padding", 0),
        FloatParameter("value", "Value", 0),
    ),
    lambda in_sizes, padding, value, **_: torch.nn.ConstantPad3d(padding, value),
    constant_padding_3d_size_transformation,
)
