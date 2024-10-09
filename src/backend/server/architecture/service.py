from genericpath import isfile
import io
import os
from pathlib import Path

from pydantic import TypeAdapter
from server.architecture.desc import ArchitectureDescription
from server.architecture.loaded import LoadedArchitecture


class ArchitectureService:
    _save_path: Path
    _architecture_adapter: TypeAdapter[ArchitectureDescription]

    def __init__(self, save_path: Path) -> None:
        self._save_path = save_path
        self._architecture_adapter = TypeAdapter(ArchitectureDescription)

        self._save_path.mkdir(parents=True, exist_ok=True)

    def save_architecture(
        self, file_name: str, architecture: ArchitectureDescription
    ) -> Path:
        """
        file name should end with '.arch.json' (but not enforced)
        """
        path = self._save_path.joinpath(file_name)
        with io.open(path, "wb") as f:
            f.write(self._architecture_adapter.dump_json(architecture))
            return path

    def delete_architecture(self, file_name: str) -> bool:
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

    def load_all_architectures(self) -> list[LoadedArchitecture]:
        """
        Tries to load all files in the save folder with the suffix '.arch.json' as an architecture.
        """
        architectures = []
        for path in os.listdir(self._save_path):
            path = self._save_path.joinpath(path)
            if path.is_file() and path.suffixes == [".arch", ".json"]:
                try:
                    architectures.append(self.load_architecture_from_path(path))
                except:
                    continue
        return architectures

    def load_architecture(self, file_name: str) -> LoadedArchitecture:
        path = self._save_path.joinpath(file_name)
        return self.load_architecture_from_path(path)

    def load_architecture_from_path(self, path: Path) -> LoadedArchitecture:
        with io.open(path, "r") as f:
            return LoadedArchitecture(
                path.name, self._architecture_adapter.validate_json(f.read())
            )
