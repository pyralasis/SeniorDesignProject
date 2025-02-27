import torch
from server.data.transforms.base import ValueTransformDefinition
from torchvision.transforms.transforms import ToTensor

image_to_tensor_transform = ValueTransformDefinition("image_to_tensor", "Image To Tensor", (), lambda **_: ToTensor())
to_tensor_transform = ValueTransformDefinition(
    "to_tensor", "Python To Tensor", (), lambda **_: (lambda val: torch.tensor(val))
)
