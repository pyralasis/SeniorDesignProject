from dataclasses import asdict, dataclass
from typing import Literal

from pydantic import TypeAdapter, ValidationError
from quart import Blueprint, ResponseReturnValue, request
from quart.views import MethodView
from server.data.service import DataService
from server.data.sources.base import DataSourceDescription, DataSourceId
from server.data.transforms.base import TransformDescription, TransformId
from server.util.file import create_object_blueprint


def create_data_blueprint(
    data_service: DataService,
) -> Blueprint:
    bp = Blueprint("data", __name__)

    bp.add_url_rule(
        "/available_sources",
        view_func=AvailableSourcesView.as_view("available_sources", data_service),
    )
    bp.add_url_rule(
        "/get_source",
        view_func=GetSourceView.as_view("get_source", data_service),
    )

    bp.add_url_rule(
        "/available_transforms",
        view_func=AvailableTransformsView.as_view("available_transforms", data_service),
    )
    bp.add_url_rule(
        "/get_transform",
        view_func=GetTransformView.as_view("get_transform", data_service),
    )

    bp.register_blueprint(create_object_blueprint(data_service.pipelines))

    return bp


###
### GENERAL
###


@dataclass
class InvalidRequestErrResponse:
    msg: str
    success: Literal[False] = False
    error_type: Literal["invalid_request"] = "invalid_request"


###
### Available Transforms View
###

AvailableTransformsResponse = list[TransformDescription]


class AvailableTransformsView(MethodView):
    init_every_request = False

    def __init__(self, data_service: DataService):
        self.data_service = data_service

    async def get(self) -> AvailableTransformsResponse:
        available_transforms = self.data_service.transforms.available()
        descriptions: AvailableTransformsResponse = list(
            map(lambda transform: transform.description(), available_transforms)
        )
        return descriptions


###
### Get Transform View
###


@dataclass
class InvalidTransformErrResponse:
    msg: str
    success: Literal[False] = False
    error_type: Literal["invalid_transform"] = "invalid_transform"


@dataclass
class GetTransformArgs:
    id: TransformId


@dataclass
class GetTransformOkResponse:
    transform: TransformDescription
    success: Literal[True] = True


class GetTransformView(MethodView):
    init_every_request = False

    def __init__(self, data_service: DataService):
        self.service = data_service
        self.adapter = TypeAdapter(GetTransformArgs)

    async def get(self) -> ResponseReturnValue:
        try:
            args = self.adapter.validate_python(request.args.to_dict())
            if self.service.transforms.contains(args.id):
                return asdict(GetTransformOkResponse(self.service.transforms.get(args.id).description()))
            else:
                return asdict(InvalidTransformErrResponse(f"No transform found with id '{args.id}'")), 400

        except ValidationError as err:
            return asdict(InvalidRequestErrResponse(str(err))), 400


###
### Available Sources View
###

AvailableSourcesResponse = list[DataSourceDescription]


class AvailableSourcesView(MethodView):
    init_every_request = False

    def __init__(self, data_service: DataService):
        self.data_service = data_service

    async def get(self):
        available_transforms = self.data_service.sources.available()
        descriptions: AvailableSourcesResponse = list(
            map(lambda transform: transform.description(), available_transforms)
        )
        return descriptions


###
### Get Source View
###


@dataclass
class InvalidSourceErrResponse:
    msg: str
    success: Literal[False] = False
    error_type: Literal["invalid_source"] = "invalid_source"


@dataclass
class GetSourceArgs:
    id: DataSourceId


@dataclass
class GetSourceOkResponse:
    source: DataSourceDescription
    success: Literal[True] = True


class GetSourceView(MethodView):
    init_every_request = False

    def __init__(self, data_service: DataService):
        self.service = data_service
        self.adapter = TypeAdapter(GetSourceArgs)

    async def get(self) -> ResponseReturnValue:
        try:
            args = self.adapter.validate_python(request.args.to_dict())
            if self.service.sources.contains(args.id):
                return asdict(GetSourceOkResponse(self.service.sources.get(args.id).description()))
            else:
                return asdict(InvalidSourceErrResponse(f"No source found with id '{args.id}'")), 400

        except ValidationError as err:
            return asdict(InvalidRequestErrResponse(str(err))), 400
