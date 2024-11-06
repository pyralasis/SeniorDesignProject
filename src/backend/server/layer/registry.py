from server.layer import LayerDefinition, LayerID


class LayerRegistry:
    _available_layers: dict[LayerID, LayerDefinition]

    def __init__(self, layers: list[LayerDefinition]) -> None:
        self._available_layers = {}

        for layer in layers:
            self.add_layer(layer)

    def add_layer(self, layer: LayerDefinition):
        self._available_layers[layer.id] = layer

    def available_layers(self) -> list[LayerDefinition]:
        return list(self._available_layers.values())

    def contains(self, id: LayerID) -> bool:
        return id in self._available_layers

    def layer(self, id: LayerID) -> LayerDefinition:
        return self._available_layers[id]
