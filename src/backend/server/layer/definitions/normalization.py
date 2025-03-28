from math import floor

import torch
from server.layer import LayerDefinition
from server.layer.input import InputDefinition
from server.layer.size import TensorSize, size_identity
from server.params import BoolParameter, FloatParameter, IntParameter, Size2DParameter, StringParameter
from server.params.constraints import OneOf, WithRange

# found here: https://pytorch.org/docs/stable/nn.html#normalization-layers

batchnorm1d_layer = LayerDefinition(
    "batchnorm1d",
    "Batch Norm 1D",
    (InputDefinition(None, 2, 3),),
    (
        IntParameter("num_features", "Num Features", 1),
        FloatParameter(id="eps", name="Eps", default=0.00005),
        FloatParameter(id="momentum", name="Momentum", default=0.1),
        BoolParameter("affine", "Affine", True),
        BoolParameter("track_running_stats ", "Track Running Stats ", True),
    ),
    lambda in_sizes, num_features, eps, momentum, affine, track_running_stats, **_: (
        torch.nn.BatchNorm1d(
            num_features,
            eps,
            momentum,
            affine,
            track_running_stats
        )
    ),
    lambda in_sizes, **_: in_sizes[0],
)

batchnorm2d_layer = LayerDefinition(
    "batchnorm2d",
    "Batch Norm 2D",
    (InputDefinition(None, 2, 3),),
    (
        IntParameter("num_features", "Num Features", 1),
        FloatParameter(id="eps", name="Eps", default=0.00005),
        FloatParameter(id="momentum", name="Momentum", default=0.1),
        BoolParameter("affine", "Affine", True),
        BoolParameter("track_running_stats ", "Track Running Stats ", True),
    ),
    lambda in_sizes, num_features, eps, momentum, affine, track_running_stats, **_: (
        torch.nn.BatchNorm2d(
            num_features,
            eps,
            momentum,
            affine,
            track_running_stats
        )
    ),
    lambda in_sizes, **_: in_sizes[0],
)

batchnorm3d_layer = LayerDefinition(
    "batchnorm3d",
    "Batch Norm 3D",
    (InputDefinition(None, 2, 3),),
    (
        IntParameter("num_features", "Num Features", 1),
        FloatParameter(id="eps", name="Eps", default=0.00005),
        FloatParameter(id="momentum", name="Momentum", default=0.1),
        BoolParameter("affine", "Affine", True),
        BoolParameter("track_running_stats ", "Track Running Stats ", True),
    ),
    lambda in_sizes, num_features, eps, momentum, affine, track_running_stats, **_: (
        torch.nn.BatchNorm3d(
            num_features,
            eps,
            momentum,
            affine,
            track_running_stats
        )
    ),
    lambda in_sizes, **_: in_sizes[0],
)