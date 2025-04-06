from dataclasses import asdict, dataclass
from typing import Literal, Optional

from pydantic import TypeAdapter, ValidationError
from quart import Blueprint, ResponseReturnValue, request
from quart.views import MethodView
from server.architecture.config import ArchitectureConfig
from server.architecture.service import ArchitectureService
from server.model.service import ModelService
from server.model.train import TrainingConfig
from server.util.file import FileId
from server.util.file.blueprint import (
    AvailableFilesView,
    AvailableObjectsView,
    LoadObjectView,
    ParseErrResponse,
    create_file_blueprint,
    create_object_blueprint,
)
from server.util.file.meta import MetaData
from server.util.registry_blueprint import create_registry_blueprint


def create_model_blueprint(model_service: ModelService, architecture_service: ArchitectureService) -> Blueprint:
    bp = Blueprint("model", __name__)

    bp.add_url_rule("/create", view_func=CreateModelView.as_view("create", model_service, architecture_service))

    # Adds available and delete endpoints, as well as metadata endpoints
    bp.register_blueprint(create_object_blueprint(model_service.models, False))

    bp.register_blueprint(
        create_registry_blueprint(model_service.loss_fns, "loss"),
        url_prefix="/loss",
    )

    bp.register_blueprint(
        create_registry_blueprint(model_service.optimizers, "optimizers"),
        url_prefix="/optimizer",
    )

    # Training
    bp_train = Blueprint("train", __name__)
    bp_train.add_url_rule("/start", view_func=TrainModelView.as_view("start", model_service))
    bp_train.add_url_rule("/delete", view_func=DeleteTrainLogView.as_view("delete", model_service))

    # Train Objects
    bp_train.add_url_rule("/available", view_func=AvailableObjectsView.as_view(f"available", model_service.train_logs))
    bp_train.add_url_rule("/load", view_func=LoadObjectView.as_view(f"load", model_service.train_logs))

    # Train status files
    bp_train.register_blueprint(
        create_file_blueprint(model_service.train_logs.data_files, model_service.train_logs, False),  # type: ignore
        url_prefix=f"/data",
    )

    # Training meta files
    bp_train.register_blueprint(
        create_file_blueprint(model_service.train_logs.meta_files, model_service.train_logs), url_prefix=f"/meta"
    )

    # Training config files
    bp_train.register_blueprint(
        create_file_blueprint(model_service.train_logs.extra_files[0], model_service.train_logs, False),
        url_prefix=f"/config",
    )

    bp_train.add_url_rule("/devices", view_func=GetDevicesView.as_view("devices", model_service))

    bp.register_blueprint(bp_train, url_prefix="/train")

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
    meta: MetaData
    config: TrainingConfig


@dataclass
class TrainModelSuccessResponse:
    log_id: FileId
    success: Literal[True] = True


@dataclass
class TrainModelErrorInvalidModel:
    success: Literal[False] = False
    error: Literal["invalid_model_id"] = "invalid_model_id"


@dataclass
class TrainModelErrorInvalidSource:
    success: Literal[False] = False
    error: Literal["invalid_source_id"] = "invalid_source_id"


class TrainModelView(MethodView):
    init_every_request = False

    def __init__(self, model_service: ModelService):
        self.service = model_service
        self.adapter = TypeAdapter(TrainModelRequestBody)

    async def post(self) -> ResponseReturnValue:
        req = self.adapter.validate_python(await request.json)

        if not self.service.models.exists(req.config.model_id):
            return asdict(TrainModelErrorInvalidModel())

        if not self.service.data_service.pipelines.exists(req.config.source_id):
            return asdict(TrainModelErrorInvalidSource())

        log_id = await self.service.add_to_training_queue(req.config, req.meta)
        return asdict(TrainModelSuccessResponse(log_id))


GetDevicesResponse = list[str]


class GetDevicesView(MethodView):
    init_every_request = False

    def __init__(self, model_service: ModelService):
        self.service = model_service

    async def get(self) -> GetDevicesResponse:
        return self.service.available_devices()

###
### Train Model View
###


@dataclass
class DeleteTrainLogRequestArgs:
    id: FileId

@dataclass
class DeleteTrainSuccessResponse:
    success: Literal[True] = True

@dataclass
class TrainInvalidIdError:
    success: Literal[False] = False
    error: Literal["invalid_id"] = "invalid_id"


@dataclass
class DeleteInProgressTrainError:
    success: Literal[False] = False
    error: Literal["delete_in_progress"] = "delete_in_progress"


class DeleteTrainLogView(MethodView):
    init_every_request = False

    def __init__(self, model_service: ModelService):
        self.service = model_service
        self.adapter = TypeAdapter(DeleteTrainLogRequestArgs)

    async def post(self) -> ResponseReturnValue:
        try:
            args = self.adapter.validate_python(request.args.to_dict())

            if not self.service.train_logs.exists(args.id):
                return asdict(TrainInvalidIdError()), 400

            train_data = self.service.train_logs.get(args.id)
            if train_data.content.data.status == "in_progress" or train_data.content.data.status == "queued":
                return asdict(DeleteInProgressTrainError()), 400
            
            self.service.train_logs.delete(args.id)
            return asdict(DeleteTrainSuccessResponse())
        except ValidationError as err:
            return asdict(ParseErrResponse(str(err))), 400