from quart import ResponseReturnValue
from quart.views import MethodView

from server.layer.registry import LayerRegistry


class AvailableLayersView(MethodView):
    init_every_request = False

    def __init__(self, layer_registry: LayerRegistry):
        self.registry = layer_registry

    async def get(self) -> ResponseReturnValue:
        available_layers = self.registry.available_layers()
        return list(map(lambda layer: layer.description(), available_layers))
