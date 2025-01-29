from typing import Any, Literal

from pydantic import TypeAdapter, ValidationError
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
    bp.add_url_rule(
        "/get",
        view_func=GetLayerView.as_view("get", layer_service),
    )

    return bp


###
### GENERAL
###


@dataclass
class InvalidLayerErrResponse:
    msg: str
    success: Literal[False] = False
    error_type: Literal["invalid_layer"] = "invalid_layer"


@dataclass
class InvalidRequestErrResponse:
    msg: str
    success: Literal[False] = False
    error_type: Literal["invalid_request"] = "invalid_request"


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
            return asdict(InvalidLayerErrResponse(f"No layer found with id '{req.layer_id}'"))

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


###
### Get Layer View
###


@dataclass
class GetLayerArgs:
    id: LayerID


@dataclass
class GetLayerOkResponse:
    layer: LayerDescription
    success: Literal[True] = True


class GetLayerView(MethodView):
    init_every_request = False

    def __init__(self, layer_service: LayerService):
        self.service = layer_service
        self.adapter = TypeAdapter(GetLayerArgs)

    async def get(self) -> ResponseReturnValue:
        try:
            args = self.adapter.validate_python(request.args.to_dict())
            if self.service.layers.contains(args.id):
                return asdict(GetLayerOkResponse(self.service.layers.get(args.id).description()))
            else:
                return asdict(InvalidLayerErrResponse(f"No layer found with id '{args.id}'")), 400

        except ValidationError as err:
            return asdict(InvalidRequestErrResponse(str(err))), 400
