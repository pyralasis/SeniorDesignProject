import torch
from server.layer import LayerDefinition
from server.layer.input import InputDefinition
from server.params import BoolParameter, FloatParameter

# found here: https://pytorch.org/docs/stable/nn.html#normalization-layers

batchnorm1d_layer = LayerDefinition(
    "batchnorm1d",
    "Batch Norm 1D",
    (InputDefinition(None, 1, 2),),
    (
        FloatParameter(id="eps", name="Eps", default=0.00005),
        FloatParameter(id="momentum", name="Momentum", default=0.1),
        BoolParameter("affine", "Affine", True),
        BoolParameter("track_running_stats ", "Track Running Stats ", True),
    ),
    lambda in_sizes, eps, momentum, affine, track_running_stats, **_: (
        torch.nn.BatchNorm1d(in_sizes[0][0], eps, momentum, affine, track_running_stats)
    ),
    lambda in_sizes, **_: in_sizes[0],
)

batchnorm2d_layer = LayerDefinition(
    "batchnorm2d",
    "Batch Norm 2D",
    (InputDefinition(None, 3, 3),),
    (
        FloatParameter(id="eps", name="Eps", default=0.00005),
        FloatParameter(id="momentum", name="Momentum", default=0.1),
        BoolParameter("affine", "Affine", True),
        BoolParameter("track_running_stats ", "Track Running Stats ", True),
    ),
    lambda in_sizes, eps, momentum, affine, track_running_stats, **_: (
        torch.nn.BatchNorm2d(in_sizes[0][0], eps, momentum, affine, track_running_stats)
    ),
    lambda in_sizes, **_: in_sizes[0],
)

batchnorm3d_layer = LayerDefinition(
    "batchnorm3d",
    "Batch Norm 3D",
    (InputDefinition(None, 4, 4),),
    (
        FloatParameter(id="eps", name="Eps", default=0.00005),
        FloatParameter(id="momentum", name="Momentum", default=0.1),
        BoolParameter("affine", "Affine", True),
        BoolParameter("track_running_stats ", "Track Running Stats ", True),
    ),
    lambda in_sizes, num_features, eps, momentum, affine, track_running_stats, **_: (
        torch.nn.BatchNorm3d(in_sizes[0][0], num_features, eps, momentum, affine, track_running_stats)
    ),
    lambda in_sizes, **_: in_sizes[0],
)
