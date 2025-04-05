from abc import ABC
from typing import Any, Generic, TypeVar

import pandas as pd
from server.data.sources.base import DataSource, DataSourceDefinition
from server.params import StringParameter
from server.util.override_decorator import override
from torch.utils.data import Dataset

TDs = TypeVar("TDs", bound=Dataset)


class CsvSource(DataSource, Generic[TDs], ABC):
    dataset: TDs
    use_labels: bool

    def __init__(self, filepath: str):
        super().__init__()
        self.data = pd.read_csv(filepath)

        # Replace every float64 column with float32
        for col in self.data.select_dtypes(include=["float64"]).columns:
            self.data[col] = self.data[col].astype("float32")

    @override
    def _get(self, index: int) -> Any:
        return self.data.iloc[index]

    @override
    def __len__(self) -> int:
        return len(  # TODO: enforce having __len__ defined using types
            self.data  # type:ignore Most have len defined
        )


csv_source = DataSourceDefinition(
    "csv_source",
    "CSV Source",
    (StringParameter("filepath", "Filepath", ""),),
    lambda filepath, **_: CsvSource(filepath),
)
