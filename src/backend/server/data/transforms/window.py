from turtle import width
from typing import Any, final

import torch
from server.data.sources.base import DataSource
from server.data.transforms.base import DataSourceTransformDefinition
from server.params import IntParameter


@final
class OverlappingWindowDataSource(DataSource):
    """
    Takes in a DataSource that outputs tensors
    """

    def __init__(self, in_src: DataSource, width: int) -> None:
        super().__init__()
        self.in_src = in_src
        self.width = width

    def _get(self, index: int) -> Any:
        vals = []
        for i in range(index, index + self.width):
            val: torch.Tensor = self.in_src[i]
            if val.dim() == 0:
                val = val.view(-1)
            vals.append(val)
        return torch.concat(vals)

    def __len__(self) -> int:
        return len(self.in_src) - (self.width - 1)


overlapping_window_transform = DataSourceTransformDefinition(
    "overalapping_window",
    "Overlapping Window",
    (IntParameter("width", "Width", 3),),
    lambda source, width, **_: OverlappingWindowDataSource(source, width),
)
