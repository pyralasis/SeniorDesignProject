from quart import ResponseReturnValue
from quart.views import MethodView
from dataclasses import asdict, dataclass
from typing import Any, Literal
from pydantic import TypeAdapter
from server.model.service import ModelService
from server.layer import LayerID
from server.layer.size import TensorSize
from server.params import AnyParameterValue
from server.views.model import ArchitecturePath
from quart import request
from server.architecture.service import ArchitectureService

# compare to server/views/layers/output_size.py


@dataclass
class CreateModelRequestBody:
    architecture_path: ArchitecturePath
    name: str

@dataclass
class SuccessfulResponse:
    model_id: str
    success: Literal[True] = True

@dataclass
class ErrorResponse:
    success: Literal[False] = False
    error: Literal["invalid_architecture_path"] = "invalid_architecture_path"

# TODO
# - create a successful response
# - create an error response
# - validate the architecture path
# - validate the name
# - call the model service to create the model
#   - make the create model function in the model service


class CreateModelView(MethodView):
    init_every_request = False

    def __init__(self, model_service: ModelService, architecture_service: ArchitectureService):
        self.service = model_service
        self.architecture_service = architecture_service
        self.adapter = TypeAdapter(CreateModelRequestBody)

    async def post(self) -> ResponseReturnValue:
        req = self.adapter.validate_python(await request.json)

        # use the architecture service to get the architecture
        # pass the architecture and the name to the model service and store the model_id
        # return the model_id
        if not self.architecture_service.files.exists(req.architecture_path):
            return asdict(ErrorResponse())

        architecture = self.architecture_service.get(req.architecture_path)
        model_id = self.service.create_model(architecture, req.name)

        return asdict(SuccessfulResponse(model_id=model_id))
