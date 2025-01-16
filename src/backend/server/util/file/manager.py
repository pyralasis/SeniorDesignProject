import io
import os
from pathlib import Path
from typing import Generic, TypeVar

from pydantic import TypeAdapter

from server.util.file.loaded import Loaded


T = TypeVar("T")


class FileManager(Generic[T]):
    _save_path: Path
    _adapter: TypeAdapter[T]

    file_type: type[T]

    def __init__(self, save_path: Path, file_type: type[T]) -> None:
        self._save_path = save_path
        self._adapter = TypeAdapter(file_type)
        self.file_type = file_type

        self._save_path.mkdir(parents=True, exist_ok=True)

    def save(self, file_name: str, data: T) -> Path:
        path = self._save_path.joinpath(file_name)

        with io.open(path, "wb") as f:
            f.write(self._adapter.dump_json(data))
            return path

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
            if path.is_file() and path.suffixes == [".arch", ".json"]:
                try:
                    architectures.append(self.load_from_path(path))
                except:
                    continue
        return architectures

    def load(self, file_name: str) -> Loaded[T]:
        path = self._save_path.joinpath(file_name)
        return self.load_from_path(path)

    def load_from_path(self, path: Path) -> Loaded[T]:
        with io.open(path, "r") as f:
            return Loaded[T](path.name, self._adapter.validate_json(f.read()))
