from server.layer import Layer, LayerID


class LayerRegistry:
    _available_layers: dict[LayerID, Layer]

    def __init__(self, layers: list[Layer]) -> None:
        self._available_layers = {}

        for layer in layers:
            self.add_layer(layer)

    def add_layer(self, layer: Layer):
        self._available_layers[layer.id] = layer

    def available_layers(self) -> list[Layer]:
        return list(self._available_layers.values())

    def contains(self, id: LayerID) -> bool:
        return id in self._available_layers

    def layer(self, id: LayerID) -> Layer:
        return self._available_layers[id]
