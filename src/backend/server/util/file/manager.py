from abc import ABC, abstractmethod
import io
import os
from pathlib import Path
import pickle
import random
from typing import Any, Generic, TypeVar
from pydantic import TypeAdapter, ValidationError
import torch

from server.util.file.loaded import Loaded
from server.util.override_decorator import override
from .id import FileId, is_file_id

T = TypeVar("T")


class FileIdNotFoundError(Exception):
    def __init__(self, file_id: int):
        super().__init__(f"File with id {file_id} not found.")
        self.file_id = file_id


class InvalidFileFormatError(Exception):
    def __init__(self, path: Path):
        super().__init__(f"Invalid file format for file at {path}.")
        self.path = path


class BaseFileManager(ABC, Generic[T]):
    _save_path: Path

    def __init__(self, save_path: Path, extension: str) -> None:
        self._extension = extension
        self._suffixes = ["." + ext for ext in extension.split(".")]
        self._save_path = save_path
        self._save_path.mkdir(parents=True, exist_ok=True)

    def create(self, data: T) -> FileId:
        """
        Creates a new file with the given data. Returns the id of the file.
        """

        id = self._generate_id()
        path = self._to_path(id)
        self._save_to_path(path, data)

        return id

    def update(self, id: int, data: T):
        """
        Updates the file with the given id to the new data.
        """

        if not self.exists(id):
            raise FileIdNotFoundError(id)

        path = self._to_path(id)
        self._save_to_path(path, data)

    @abstractmethod
    def _save_to_path(self, path: Path, data: T): ...

    def delete(self, id: int):
        """
        Deletes the file with the given id.
        """
        if not self.exists(id):
            raise FileIdNotFoundError(id)

        path = self._to_path(id)
        os.remove(path)

    def available(self) -> list[FileId]:
        """
        Returns a list of all available file id's.
        """
        ids = []
        for path in os.listdir(self._save_path):
            path = self._save_path.joinpath(path)
            id_str = path.name.split(".")[0]
            if path.is_file() and path.suffixes == self._suffixes and is_file_id(id_str):
                ids.append(int(id_str))
        return ids

    def load_all(self) -> list[Loaded[T]]:
        """
        Tries to load all available files in the save folder.
        """
        values = []
        for id in self.available():
            try:
                values.append(self.load(id))
            except:
                continue
        return values

    def load(self, id: FileId) -> Loaded[T]:
        path = self._to_path(id)
        return Loaded[T](id, self._load_from_path(path))

    @abstractmethod
    def _load_from_path(self, path: Path) -> T: ...

    def exists(self, id: FileId) -> bool:
        return os.path.exists(self._to_path(id))

    def _to_path(self, id: FileId) -> Path:
        return self._save_path.joinpath(f"{id}" + self._extension)

    def _generate_id(self) -> FileId:
        id = random.randint(1, 1000000000)

        while self.exists(id):
            id = random.randint(1, 1000000000)

        return id


class JsonFileManager(BaseFileManager[T], Generic[T]):
    _adapter: TypeAdapter[T]
    file_type: type[T]

    def __init__(self, save_path: Path, file_type: type[T], extension: str) -> None:
        self._adapter = TypeAdapter(file_type)
        self.file_type = file_type
        super().__init__(save_path, extension)

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


class TorchWeightsFileManager(BaseFileManager[dict[str, Any]]):
    def __init__(self, save_path: Path, extension: str) -> None:
        super().__init__(save_path, extension)

    @override
    def _save_to_path(self, path: Path, data: dict[str, Any]):
        torch.save(data, path)

    @override
    def _load_from_path(self, path: Path) -> dict[str, Any]:
        try:
            return torch.load(path)
        except (ValueError, RuntimeError, pickle.UnpicklingError):
            raise InvalidFileFormatError(path)
