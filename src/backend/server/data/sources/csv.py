from torch.utils.data import Dataset
from server.params import StringParameter
from server.data.sources.base import DataSource, DataSourceDefinition
from server.util.override_decorator import override

from abc import ABC
from typing import Any, Generic, TypeVar

import pandas as pd

TDs = TypeVar("TDs", bound=Dataset)


class CsvSource(DataSource, Generic[TDs], ABC):
    dataset: TDs
    use_labels: bool

    def __init__(self, filepath: str):
        super().__init__()
        self.data = pd.read_csv(filepath)

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