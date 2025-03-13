from dataclasses import asdict, dataclass
from typing import Literal

from pydantic import TypeAdapter
from quart import Blueprint, ResponseReturnValue, request
from quart.views import MethodView
from server.architecture.config import ArchitectureConfig
from server.architecture.service import ArchitectureService
from server.model.service import ModelService
from server.util.file import FileId
from server.util.file.blueprint import AvailableObjectsView, create_file_blueprint
from server.util.file.meta import MetaData


def create_model_blueprint(model_service: ModelService, architecture_service: ArchitectureService) -> Blueprint:
    bp = Blueprint("model", __name__)

    bp.add_url_rule("/create", view_func=CreateModelView.as_view("create", model_service, architecture_service))
    bp.add_url_rule("/available", view_func=AvailableObjectsView.as_view("available", model_service.models))

    # Allows for editing meta data
    bp.register_blueprint(
        create_file_blueprint(model_service.models.meta_files, model_service.models),
        url_prefix=f"/{model_service.models.meta_files.api_name()}",
    )

    return bp


###
### Create Model View
###


@dataclass
class CreateModelRequestBody:
    architecture_id: FileId
    meta: MetaData


@dataclass
class SuccessfulResponse:
    model_id: FileId
    success: Literal[True] = True


@dataclass
class ErrorResponseInvalidArchitecture:
    success: Literal[False] = False
    error: Literal["invalid_architecture_id"] = "invalid_architecture_id"


@dataclass
class ErrorResponseModelCreationFailure:
    success: Literal[False] = False
    error: Literal["model_creation_failure"] = "model_creation_failure"


# TODO
# - create a successful response
# - create an error response
# - validate the architecture path
# - validate the name
# - call the model service to create the model
#   - make the create model function in the model service


# compare to server/util/file/blueprint.py or server/views/layers.py (OutputSizeView)
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
        if not self.architecture_service.architectures.exists(req.architecture_id):
            return asdict(ErrorResponseInvalidArchitecture())

        # feel free to create a wrapper function on the architecture service for this
        """
        The view receives a request with the architecture_id
        Use architecture service to get the architecture config
        Pass architecture config to model service
        Model service creates the model and returns any relevant info (probably model_id)
        The view responds with whatever info needed
        """
        try:
            loaded_architecture: ArchitectureConfig = self.architecture_service.load_architecture(req.architecture_id)
            model_id = self.service.create_model(loaded_architecture, req.meta)
        except:
            return asdict(ErrorResponseModelCreationFailure())

        return asdict(SuccessfulResponse(model_id=model_id))
