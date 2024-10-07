import io

from pydantic import RootModel, TypeAdapter
from backend.server.architecture.layers import Layer, LayerID
from server.architecture.desc import ArchitectureDescription


class ArchitectureService:
    _available_layers: dict[LayerID, Layer]
    _architecture_adapter: TypeAdapter[ArchitectureDescription]

    def __init__(self, layers: list[Layer]) -> None:
        self._available_layers = {}
        self._architecture_adapter = TypeAdapter(ArchitectureDescription)

        for layer in layers:
            self.add_layer(layer)

    def add_layer(self, layer: Layer):
        self._available_layers[layer.id] = layer

    def available_layers(self) -> list[Layer]:
        return list(self._available_layers.values())

    def layer(self, id: LayerID) -> Layer:
        return self._available_layers[id]

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
