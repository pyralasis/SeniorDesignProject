from dataclasses import dataclass
from typing import Any
import pandas as pd
import torch
from server.params import Size2D, Size2DParameter
from server.data.transforms.base import ValueTransformDefinition
from torchvision.transforms.transforms import ToTensor

@dataclass
class ColumnRangeTransform:
    range: Size2D

    def __call__(self, df: pd.Series) -> Any:
        return df.iloc[int(self.range[0]):int(self.range[1])]

df_column_range_transform = ValueTransformDefinition(
    "df_column_range", "Dataframe Column Range", (Size2DParameter(id="range", name="Range", default=(0,1)),), 
    lambda range, **_: ColumnRangeTransform(range)
)

class DfStringToTransform:
    mapping: dict[str, int]
    next: int

    def __init__(self) -> None:
        self.mapping = {}
        self.next = 0

    def __call__(self, df: pd.Series) -> Any:

        for i in range(len(df.values)):
            val = df.values[i]
            if isinstance(val, str):
                if val not in self.mapping:
                    self.mapping[val] = self.next
                    self.next += 1
                df.iat[i] = self.mapping[val]

        return df

df_string_to_number_transform = ValueTransformDefinition(
    "df_string_to_number", "Dataframe String to Number", (), 
    lambda **_: DfStringToTransform()
)
