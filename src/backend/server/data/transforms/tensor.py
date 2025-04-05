import torch
from server.data.transforms.base import ValueTransformDefinition
from server.params import FloatParameter
from sympy import Float
from torchvision import transforms

squeeze_transform = ValueTransformDefinition("squeeze", "Squeeze", (), lambda **_,: torch.squeeze)

normalize_transform = ValueTransformDefinition(
    "normalize",
    "Normalize",
    (
        FloatParameter("mean", "Mean", default=0),
        FloatParameter("std_dev", "Standard Deviation", default=1),
    ),
    lambda mean, std_dev, **_: transforms.Normalize((mean,), (std_dev,)),
)
