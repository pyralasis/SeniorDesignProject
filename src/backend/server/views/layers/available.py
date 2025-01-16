from quart import ResponseReturnValue
from quart.views import MethodView

from server.layer import LayerDefinition, LayerDescription
from server.util.registry import Registry

Response = list[LayerDescription]


class AvailableLayersView(MethodView):
    init_every_request = False

    def __init__(self, layer_registry: Registry[LayerDefinition]):
        self.registry = layer_registry

    async def get(self) -> ResponseReturnValue:
        available_layers = self.registry.available()
        descriptions: Response = list(map(lambda layer: layer.description(), available_layers))
        return descriptions
