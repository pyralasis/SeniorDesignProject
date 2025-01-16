__all__ = ["default_sources", "DataSource", "DataSourceDefinition", "DataSourceDescription", "DataSourceId", "DS_ROOT"]

from .mnist import mnist_values, mnist_labels
from .base import DataSource, DataSourceDefinition, DataSourceDescription, DataSourceId, DS_ROOT

default_sources: list[DataSourceDefinition] = [mnist_values, mnist_labels]
