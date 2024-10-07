from collections import namedtuple
from typing import TYPE_CHECKING, Generic, Literal, LiteralString, NamedTuple, TypeVar
import torch
import torch.nn as nn

# Create a 2D tensor of ones (e.g., with size 1x1x4x4, resembling a single-channel 4x4 image)
input_tensor = torch.ones(1, 1, 4, 4)

# Define a 2D max pooling layer (with kernel_size=2, stride=2 for this example)
max_pool = nn.MaxPool2d(kernel_size=2, stride=2)

# Apply max pooling to the input tensor
output_tensor: torch.Tensor = max_pool(input_tensor)

# Print the input and output tensors
print("Input Tensor:")
print(input_tensor.size())
print(input_tensor)
print("\nOutput Tensor after Max Pooling:")
print(output_tensor.size())
print(output_tensor)