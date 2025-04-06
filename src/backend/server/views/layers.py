from dataclasses import asdict, dataclass
from typing import Any, Literal

from pydantic import TypeAdapter, ValidationError
from quart import Blueprint, ResponseReturnValue, request
from quart.views import MethodView
from server.layer import LayerDescription, LayerID
from server.layer.service import LayerService
from server.layer.size import TensorSize
from server.params import AnyParameterValue
from server.util.errors import InvalidRequestErrResponse
from server.util.params import get_params_dict
from server.util.registry_blueprint import (
    InvalidItemErrResponse,
    create_registry_blueprint,
)


def create_layer_blueprint(layer_service: LayerService) -> Blueprint:
    bp = Blueprint("layer", __name__)

    bp.register_blueprint(create_registry_blueprint(layer_service.layers, "layers"))

    bp.add_url_rule(
        "/output_size",
        view_func=LayerOutputSizeView.as_view("output_size", layer_service),
    )

    return bp


###
### GENERAL
###


###
### OUTPUT SIZE VIEW
###


@dataclass
class LayerOutputSizeRequestBody:
    layer_id: LayerID
    input_size: TensorSize
    parameters: list[tuple[str, AnyParameterValue]]


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
        try:
            req = self.adapter.validate_python(await request.json)

            if not self.service.layers.contains(req.layer_id):
                return asdict(InvalidItemErrResponse(f"No layer found with id '{req.layer_id}'"))

            layer = self.service.layers.get(req.layer_id)

            out_size = layer.size((req.input_size,), **get_params_dict(req.parameters))

            return asdict(SuccessfulLayerOutputSizeResponse(out_size))

        except ValidationError as err:
            return asdict(InvalidRequestErrResponse(str(err))), 400
