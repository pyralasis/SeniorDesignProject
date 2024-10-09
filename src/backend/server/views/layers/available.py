from quart import ResponseReturnValue
from quart.views import MethodView

from server.layer import LayerDescription
from server.layer.registry import LayerRegistry

Response = list[LayerDescription]

class AvailableLayersView(MethodView):
    init_every_request = False

    def __init__(self, layer_registry: LayerRegistry):
        self.registry = layer_registry

    async def get(self) -> ResponseReturnValue:
        available_layers = self.registry.available_layers()
        descriptions: Response = list(map(lambda layer: layer.description(), available_layers))
        return descriptions
