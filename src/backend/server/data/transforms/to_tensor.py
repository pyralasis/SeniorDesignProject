from torchvision.transforms.transforms import ToTensor
from server.data.transforms.base import ValueTransformDefinition

to_tensor_transform = ValueTransformDefinition("to_tensor", "To Tensor", (), lambda **_: ToTensor())
