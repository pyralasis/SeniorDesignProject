from typing import Any, Literal

from pydantic import TypeAdapter
from quart.views import MethodView
from server.layer import LayerDescription, LayerID
from dataclasses import asdict, dataclass
from server.layer.service import LayerService
from server.layer.size import TensorSize
from server.params import AnyParameterValue


from quart import Blueprint, ResponseReturnValue, request


def create_layer_blueprint(layer_service: LayerService) -> Blueprint:
    bp = Blueprint("layer", __name__)

    bp.add_url_rule(
        "/available",
        view_func=AvailableLayersView.as_view("available_layers", layer_service),
    )
    bp.add_url_rule(
        "/output_size",
        view_func=LayerOutputSizeView.as_view("output_size", layer_service),
    )

    return bp


###
### GENERAL
###


@dataclass
class InvalidLayerResponse:
    success: Literal[False] = False
    error: Literal["invalid_layer"] = "invalid_layer"


###
### OUTPUT SIZE VIEW
###


@dataclass
class LayerOutputSizeRequestBody:
    layer_id: LayerID
    input_size: TensorSize
    parameters: dict[str, AnyParameterValue]


@dataclass
class SuccessfulLayerOutputSizeResponse:
    output_size: TensorSize
    success: Literal[True] = True


# TODO
# I am currently assuming the parameters are correct. Instead, it might make sense to either validate the parameter
# types manually or use a metaclass to create a type that allows the TypeAdapter to validate the parameters.


class LayerOutputSizeView(MethodView):
    init_every_request = False

    def __init__(self, layer_service: LayerService):
        self.service = layer_service
        self.adapter = TypeAdapter(LayerOutputSizeRequestBody)

    async def post(self) -> ResponseReturnValue:
        req = self.adapter.validate_python(await request.json)

        if not self.service.layers.contains(req.layer_id):
            return asdict(InvalidLayerResponse())

        layer = self.service.layers.get(req.layer_id)
        size_arguments: list[Any] = [req.input_size]

        for param in layer.parameters:
            size_arguments.append(req.parameters[param.id].val if param.id in req.parameters else param.default)

        out_size = layer.size(*size_arguments)

        return asdict(SuccessfulLayerOutputSizeResponse(out_size))


###
### Available Layers
###


AvailableLayersResponse = list[LayerDescription]


class AvailableLayersView(MethodView):
    init_every_request = False

    def __init__(self, layer_service: LayerService):
        self.service = layer_service

    async def get(self) -> ResponseReturnValue:
        available_layers = self.service.layers.available()
        descriptions: AvailableLayersResponse = list(map(lambda layer: layer.description(), available_layers))
        return descriptions
