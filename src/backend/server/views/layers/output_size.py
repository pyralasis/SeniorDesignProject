from dataclasses import asdict, dataclass
from typing import Any, Literal
from pydantic import TypeAdapter
from quart import ResponseReturnValue, request
from quart.views import MethodView

from server.layer import LayerID
from server.params import AnyParameterValue
from server.layer.registry import LayerRegistry
from server.layer.size import TensorSize


@dataclass
class LayerOutputSizeRequestBody:
    layer_id: LayerID
    input_size: TensorSize
    parameters: dict[str, AnyParameterValue]


@dataclass
class SuccessfulResponse:
    output_size: TensorSize
    success: Literal[True] = True


@dataclass
class InvalidLayerResponse:
    success: Literal[False] = False
    error: Literal["invalid_layer"] = "invalid_layer"


# TODO
# I am currently assuming the parameters are correct. Instead, it might make sense to either validate the parameter
# types manually or use a metaclass to create a type that allows the TypeAdapter to validate the parameters.


class LayerOutputSizeView(MethodView):
    init_every_request = False

    def __init__(self, layer_registry: LayerRegistry):
        self.registry = layer_registry
        self.adapter = TypeAdapter(LayerOutputSizeRequestBody)

    async def post(self) -> ResponseReturnValue:
        req = self.adapter.validate_python(await request.json)

        if not self.registry.contains(req.layer_id):
            return asdict(InvalidLayerResponse())

        layer = self.registry.layer(req.layer_id)
        size_arguments: list[Any] = [req.input_size]

        for param in layer.parameters:
            size_arguments.append(
                req.parameters[param.id].val
                if param.id in req.parameters
                else param.default
            )

        out_size = layer.size(*size_arguments)

        return asdict(SuccessfulResponse(out_size))
