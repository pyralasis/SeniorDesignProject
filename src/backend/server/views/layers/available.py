from quart import ResponseReturnValue
from quart.views import MethodView

from server.layer import LayerDescription
from server.layer.service import LayerService

Response = list[LayerDescription]


class AvailableLayersView(MethodView):
    init_every_request = False

    def __init__(self, layer_service: LayerService):
        self.service = layer_service

    async def get(self) -> ResponseReturnValue:
        available_layers = self.service.layers.available()
        descriptions: Response = list(map(lambda layer: layer.description(), available_layers))
        return descriptions
