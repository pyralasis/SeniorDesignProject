from dataclasses import asdict, dataclass
from typing import Literal, Optional

from pydantic import TypeAdapter
from quart import Blueprint, ResponseReturnValue, request
from quart.views import MethodView
from server.architecture.config import ArchitectureConfig
from server.architecture.service import ArchitectureService
from server.model.service import ModelService, TrainingConfig
from server.util.file import FileId
from server.util.file.blueprint import create_object_blueprint
from server.util.file.meta import MetaData


def create_model_blueprint(model_service: ModelService, architecture_service: ArchitectureService) -> Blueprint:
    bp = Blueprint("model", __name__)

    bp.add_url_rule("/create", view_func=CreateModelView.as_view("create", model_service, architecture_service))
    bp.add_url_rule("/train", view_func=TrainModelView.as_view("train", model_service))

    # Adds available and delete endpoints, as well as metadata endpoints
    bp.register_blueprint(create_object_blueprint(model_service.models, False))

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


###
### Train Model View
###


@dataclass
class TrainModelRequestBody:
    model_id: FileId
    source_id: FileId
    learning_rate: Optional[float] = None
    batch_size: Optional[int] = None
    epochs: Optional[int] = None


@dataclass
class TrainModelSuccessResponse:
    success: Literal[True] = True


@dataclass
class TrainModelErrorInvalidModel:
    success: Literal[False] = False
    error: Literal["invalid_model_id"] = "invalid_model_id"


@dataclass
class TrainModelErrorInvalidSource:
    success: Literal[False] = False
    error: Literal["invalid_source_id"] = "invalid_source_id"


@dataclass
class TrainModelErrorTrainingFailure:
    success: Literal[False] = False
    error: Literal["training_failure"] = "training_failure"


class TrainModelView(MethodView):
    init_every_request = False

    def __init__(self, model_service: ModelService):
        self.service = model_service
        self.adapter = TypeAdapter(TrainModelRequestBody)

    async def post(self) -> ResponseReturnValue:
        req = self.adapter.validate_python(await request.json)

        if not self.service.models.exists(req.model_id):
            return asdict(TrainModelErrorInvalidModel())

        if not self.service.data_service.pipelines.exists(req.source_id):
            return asdict(TrainModelErrorInvalidSource())

        try:
            # Create training config with any provided overrides
            config = TrainingConfig()
            if req.learning_rate is not None:
                config.learning_rate = req.learning_rate
            if req.batch_size is not None:
                config.batch_size = req.batch_size
            if req.epochs is not None:
                config.epochs = req.epochs

            self.service.train_model(req.model_id, req.source_id, config)
            return asdict(TrainModelSuccessResponse())
        except:
            return asdict(TrainModelErrorTrainingFailure())
