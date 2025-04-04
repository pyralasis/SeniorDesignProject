import torch
from server.data.transforms.base import ValueTransformDefinition

squeeze_transform = ValueTransformDefinition(
    "squeeze", "Squeeze", (), 
    lambda **_,: torch.squeeze
)
