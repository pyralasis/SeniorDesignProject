__all__ = ["default_sources", "DataSource", "DataSourceDefinition", "DataSourceDescription", "DataSourceId", "DS_ROOT"]

from .mnist import fashion_mnist_values, fashion_mnist_labels
from .base import DataSource, DataSourceDefinition, DataSourceDescription, DataSourceId, DS_ROOT

default_sources: list[DataSourceDefinition] = [fashion_mnist_values, fashion_mnist_labels]
