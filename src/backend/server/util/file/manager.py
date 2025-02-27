import io
import os
import pickle
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar

import torch
from pydantic import TypeAdapter, ValidationError
from server.util.override_decorator import override

from .file import FileId, LoadedFile, is_file_id

T = TypeVar("T")


class FileIdNotFoundError(Exception):
    def __init__(self, file_id: int):
        super().__init__(f"File with id {file_id} not found.")
        self.file_id = file_id


class InvalidFileFormatError(Exception):
    def __init__(self, path: Path):
        super().__init__(f"Invalid file format for file at {path}.")
        self.path = path


class IFileManager(ABC, Generic[T]):
    @abstractmethod
    def save_to(self, id: int, data: T):
        """
        Saves a file with the given data.
        """
        ...

    @abstractmethod
    def delete(self, id: int):
        """
        Deletes the file with the given id.
        """
        ...

    @abstractmethod
    def available(self) -> list[FileId]:
        """
        Returns a list of all available file id's.
        """
        ...

    @abstractmethod
    def load_all(self) -> list[LoadedFile[T]]:
        """
        Tries to load all available files in the save folder.
        """
        ...

    @abstractmethod
    def load(self, id: FileId) -> T: ...

    @abstractmethod
    def exists(self, id: FileId) -> bool: ...


class INetworkFileManager(IFileManager[T], ABC, Generic[T]):
    @abstractmethod
    def file_type(self) -> type[T]: ...

    @abstractmethod
    def api_name(self) -> str:
        """
        Returns the name of the api endpoint prefix used by this file manager.
        """
        ...


class BaseFileManager(IFileManager, ABC, Generic[T]):
    _save_path: Path
    _file_type: type[T]

    def __init__(self, name: str, save_path: Path, extension: str) -> None:
        self.name = name
        self._extension = extension
        self._suffixes = ["." + ext for ext in extension.split(".")[1:]]
        self._save_path = save_path
        self._save_path.mkdir(parents=True, exist_ok=True)

    @override
    def save_to(self, id: int, data: T):
        path = self._to_path(id)
        self._save_to_path(path, data)

    @abstractmethod
    def _save_to_path(self, path: Path, data: T): ...

    @override
    def delete(self, id: int):
        if not self.exists(id):
            raise FileIdNotFoundError(id)

        path = self._to_path(id)
        os.remove(path)

    @override
    def available(self) -> list[FileId]:
        ids = []
        for path in os.listdir(self._save_path):
            path = self._save_path.joinpath(path)
            id_str = path.name.split(".")[0]
            if path.is_file() and path.suffixes == self._suffixes and is_file_id(id_str):
                ids.append(int(id_str))
        return ids

    @override
    def load_all(self) -> list[LoadedFile[T]]:
        values = []
        for id in self.available():
            try:
                values.append(self.load(id))
            except:
                continue
        return values

    @override
    def load(self, id: FileId) -> T:
        if not self.exists(id):
            raise FileIdNotFoundError(id)

        path = self._to_path(id)
        return self._load_from_path(path)

    @abstractmethod
    def _load_from_path(self, path: Path) -> T: ...

    @override
    def exists(self, id: FileId) -> bool:
        return os.path.exists(self._to_path(id))

    @override
    def _to_path(self, id: FileId) -> Path:
        return self._save_path.joinpath(f"{id}" + self._extension)


class JsonFileManager(INetworkFileManager[T], BaseFileManager[T], Generic[T]):
    _adapter: TypeAdapter[T]
    _file_type: type[T]

    def __init__(self, name: str, save_path: Path, file_type: type[T], extension: str) -> None:
        self._adapter = TypeAdapter(file_type)
        self._file_type = file_type
        super().__init__(name, save_path, extension)

    @override
    def _save_to_path(self, path: Path, data: T):
        with io.open(path, "wb") as f:
            f.write(self._adapter.dump_json(data))

    @override
    def _load_from_path(self, path: Path) -> T:
        try:
            with io.open(path, "r") as f:
                return self._adapter.validate_json(f.read())
        except ValidationError:
            raise InvalidFileFormatError(path)

    @override
    def file_type(self) -> type:
        return self._file_type

    @override
    def api_name(self) -> str:
        return self.name


class TorchWeightsFileManager(BaseFileManager[dict[str, Any]]):
    def __init__(self, name: str, save_path: Path, extension: str) -> None:
        super().__init__(name, save_path, extension)

    @override
    def _save_to_path(self, path: Path, data: dict[str, Any]):
        torch.save(data, path)

    @override
    def _load_from_path(self, path: Path) -> dict[str, Any]:
        try:
            return torch.load(path)
        except (ValueError, RuntimeError, pickle.UnpicklingError):
            raise InvalidFileFormatError(path)
