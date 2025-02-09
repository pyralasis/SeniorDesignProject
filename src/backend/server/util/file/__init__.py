"""
A set of utilities and data structures for working with the files.
"""

__all__ = [
    "create_file_blueprint",
    "create_object_blueprint",
    "FileCoordinator",
    "IncorrectFileArgumentsError",
    "FileId",
    "LoadedFile",
    "is_file_id",
    "BaseFileManager",
    "FileIdNotFoundError",
    "IFileManager",
    "INetworkFileManager",
    "InvalidFileFormatError",
    "JsonFileManager",
    "TorchWeightsFileManager",
    "MetaData",
    "LoadableObjectProtocol",
    "LoadedObject",
    "ObjectDescription",
    "ObjectInfo",
    "Loadable",
]

from .blueprint import create_file_blueprint, create_object_blueprint
from .coordinator import FileCoordinator, IncorrectFileArgumentsError
from .file import FileId, LoadedFile, is_file_id
from .manager import (
    BaseFileManager,
    FileIdNotFoundError,
    IFileManager,
    INetworkFileManager,
    InvalidFileFormatError,
    JsonFileManager,
    TorchWeightsFileManager,
)
from .meta import MetaData
from .object import (
    Loadable,
    LoadableObjectProtocol,
    LoadedObject,
    ObjectDescription,
    ObjectInfo,
)
