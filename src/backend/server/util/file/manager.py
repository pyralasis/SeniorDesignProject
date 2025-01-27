from abc import ABC, abstractmethod
import io
import os
from pathlib import Path
from re import A
from typing import Any, Callable, Generic, TypeVar

from pydantic import TypeAdapter
import torch

from server.util.file.loaded import Loaded
from server.util.override_decorator import override


T = TypeVar("T")


class BaseFileManager(ABC, Generic[T]):
    _save_path: Path

    def __init__(self, save_path: Path, extension: str) -> None:
        self._suffixes = ["." + ext for ext in extension.split(".")]
        self._save_path = save_path
        self._save_path.mkdir(parents=True, exist_ok=True)

    def save(self, file_name: str, data: T) -> Path:
        path = self._save_path.joinpath(file_name)
        self._save_to_path(path, data)
        return path

    @abstractmethod
    def _save_to_path(self, path: Path, data: T): ...

    def delete(self, file_name: str) -> bool:
        """
        Returns whether it could be deleted.

        Note: Not really secure, pretty sure file name could be a relative path.
        """
        path = self._save_path.joinpath(file_name)
        if os.path.exists(path):
            try:
                os.remove(path)
                return True
            except:
                return False

        return False

    def load_all(self) -> list[Loaded[T]]:
        """
        Tries to load all files in the save folder with the suffix '.arch.json' as an architecture.
        """
        architectures = []
        for path in os.listdir(self._save_path):
            path = self._save_path.joinpath(path)
            if path.is_file() and path.suffixes == self._suffixes:
                try:
                    architectures.append(Loaded[T](path.name, self._load_from_path(path)))
                except:
                    continue
        return architectures

    def load(self, file_name: str) -> Loaded[T]:
        path = self._save_path.joinpath(file_name)
        return Loaded[T](path.name, self._load_from_path(path))

    @abstractmethod
    def _load_from_path(self, path: Path) -> T: ...

    @abstractmethod
    def exists(self, file_name: str) -> bool: ...


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
        with io.open(path, "r") as f:
            return self._adapter.validate_json(f.read())

    @override
    def exists(self, file_name: str) -> bool:
        return self._save_path.joinpath(file_name).exists()


class TorchWeightsFileManager(BaseFileManager[dict[str, Any]]):

    def __init__(self, save_path: Path, extension: str) -> None:
        super().__init__(save_path, extension)

    @override
    def _save_to_path(self, path: Path, data: dict[str, Any]):
        torch.save(data, path)

    @override
    def _load_from_path(self, path: Path) -> dict[str, Any]:
        return torch.load(path)

    @override
    def exists(self, file_name: str) -> bool:
        return self._save_path.joinpath(file_name).exists()
