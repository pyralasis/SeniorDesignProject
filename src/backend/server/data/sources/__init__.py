__all__ = ["default_sources", "DataSource", "DataSourceDefinition", "DataSourceDescription", "DataSourceId", "DS_ROOT"]

from .fashion_mnist import fashion_mnist_values, fashion_mnist_labels
from .mnist import mnist_values, mnist_labels
from .base import DataSource, DataSourceDefinition, DataSourceDescription, DataSourceId, DS_ROOT
from .csv import csv_source
from .emnist import emnist_labels, emnist_values

default_sources: list[DataSourceDefinition] = [fashion_mnist_values, fashion_mnist_labels, mnist_values, mnist_labels, csv_source, emnist_values, emnist_labels]
