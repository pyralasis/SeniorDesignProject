import io

from pydantic import TypeAdapter
from server.architecture.desc import ArchitectureDescription


class ArchitectureService:
    _architecture_adapter: TypeAdapter[ArchitectureDescription]

    def __init__(self) -> None:
        self._architecture_adapter = TypeAdapter(ArchitectureDescription)

    def save_architecture(
        self, name: str, architecture: ArchitectureDescription
    ) -> str:
        path = f"{name}.json"
        with io.open(path, "wb", encoding="utf-8") as f:
            f.write(self._architecture_adapter.dump_json(architecture))
            return path

    def load_architecture(self, path: str) -> ArchitectureDescription:
        with io.open(path, "r") as f:
            return self._architecture_adapter.validate_json(f.read())
