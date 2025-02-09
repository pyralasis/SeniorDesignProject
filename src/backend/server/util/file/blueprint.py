from dataclasses import asdict, dataclass
from typing import Generic, Literal, TypeVar, TypeVarTuple

from pydantic import TypeAdapter, ValidationError
from quart import Blueprint, ResponseReturnValue, request
from quart.views import MethodView

from .coordinator import FileCoordinator
from .file import FileId
from .manager import FileIdNotFoundError, INetworkFileManager, InvalidFileFormatError
from .object import LoadableObjectProtocol, ObjectDescription

###
### General
###

T = TypeVar("T")
TObj = TypeVar("TObj", bound=LoadableObjectProtocol)
TMain = TypeVar("TMain")
Ts = TypeVarTuple("Ts")


@dataclass
class ParseErrResponse:
    msg: str
    error_type: Literal["invalid_message"] = "invalid_message"
    success: Literal[False] = False


@dataclass
class InvalidIdErrResponse:
    msg: str
    error_type: Literal["invalid_id"] = "invalid_id"
    success: Literal[False] = False


@dataclass
class IOErrResponse:
    msg: str
    error_type: Literal["io"] = "io"
    success: Literal[False] = False


###
### Coordinated Files (object) Blueprint
###


def create_object_blueprint(file_coordinator: FileCoordinator) -> Blueprint:
    obj_api_name = file_coordinator.api_name
    bp = Blueprint(f"files", __name__)

    bp.add_url_rule("/available", view_func=AvailableObjectsView.as_view(f"available", file_coordinator))
    bp.add_url_rule("/delete", view_func=DeleteObjectView.as_view(f"delete", file_coordinator))
    bp.add_url_rule("/load", view_func=LoadObjectView.as_view(f"load", file_coordinator))
    bp.add_url_rule("/create", view_func=CreateObjectView.as_view(f"create", file_coordinator))
    bp.add_url_rule("/update", view_func=UpdateObjectView.as_view(f"update", file_coordinator))

    bp.register_blueprint(
        create_file_blueprint(file_coordinator.meta_files, file_coordinator),
        url_prefix=f"/{file_coordinator.meta_files.api_name()}",
    )

    # This will not work if the data FileManager is not a INetworkFileManager (e.g. you can't use this with pytorch weights)
    bp.register_blueprint(
        create_file_blueprint(file_coordinator.data_files, file_coordinator),  # type: ignore
        url_prefix=f"/{file_coordinator.data_files.api_name()}",  # type: ignore
    )

    for file_manager in file_coordinator.extra_files:
        bp.register_blueprint(
            create_file_blueprint(file_manager, file_coordinator),
            url_prefix=f"/{file_manager.api_name()}",
        )

    return bp


###
### Available Objects View
###


@dataclass
class AvailableObjectsOkResponse:
    available: list[ObjectDescription]
    success: Literal[True] = True


class AvailableObjectsView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_coord: FileCoordinator):
        self.file_coord = file_coord

    async def get(self) -> ResponseReturnValue:
        self.file_coord.available()
        try:
            return asdict(AvailableObjectsOkResponse(self.file_coord.available()))

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500


###
### Create Object View
###


TCreateRequestBody = TypeVar("TCreateRequestBody", bound=LoadableObjectProtocol)


@dataclass
class CreateOkResponse:
    id: FileId
    success: Literal[True] = True


class CreateObjectView(MethodView, Generic[TCreateRequestBody]):
    """
    View for creating a new object.

    Body of the request should be the data object which can be found in the respective object's service
    (i.e. `./server/architecture/service.py`).
    """

    init_every_request = False

    def __init__(self, file_coord: FileCoordinator):
        self.file_coord = file_coord
        self.adapter = TypeAdapter[TCreateRequestBody](file_coord.obj_type)

    async def post(self) -> ResponseReturnValue:
        try:
            # Uses validate_json and request.get_data() instead of validate_python and request.json
            # for better/easier validation
            body = self.adapter.validate_json(await request.get_data())
            id = self.file_coord.create(body)
            return asdict(CreateOkResponse(id))

        except ValidationError as err:
            return asdict(ParseErrResponse(str(err))), 400

        except FileIdNotFoundError as err:
            return asdict(InvalidIdErrResponse(str(err))), 400

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500


###
### Load Object View
###


@dataclass
class LoadObjectRequestArgs:
    id: FileId


@dataclass
class LoadObjectOkResponse(Generic[T]):
    object: T
    success: Literal[True] = True


class LoadObjectView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_coord: FileCoordinator):
        self.file_coord = file_coord
        self.adapter = TypeAdapter(LoadObjectRequestArgs)

    async def get(self) -> ResponseReturnValue:
        try:
            args = self.adapter.validate_python(request.args.to_dict())
            return asdict(LoadObjectOkResponse(self.file_coord.get(args.id)))

        except ValidationError as err:
            return asdict(ParseErrResponse(str(err))), 400

        except FileIdNotFoundError as err:
            return asdict(InvalidIdErrResponse(str(err))), 400

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500


###
### Delete Object View
###


@dataclass
class DeleteRequestBody:
    id: FileId


@dataclass
class DeleteOkResponse:
    success: Literal[True] = True


class DeleteObjectView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_coord: FileCoordinator):
        self.file_coord = file_coord
        self.adapter = TypeAdapter(DeleteRequestBody)

    async def post(self) -> ResponseReturnValue:
        try:
            body = self.adapter.validate_json(await request.get_data())
            self.file_coord.delete(body.id)
            return asdict(DeleteOkResponse())

        except ValidationError as err:
            return asdict(ParseErrResponse(str(err))), 400

        except FileIdNotFoundError as err:
            return asdict(InvalidIdErrResponse(str(err))), 400

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500


###
### Update Object View
###


@dataclass
class UpdateObjectRequestBody(Generic[TObj]):
    id: FileId
    object: TObj


@dataclass
class UpdateObjectOkResponse:
    success: Literal[True] = True


class UpdateObjectView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_coord: FileCoordinator):
        self.file_coord = file_coord
        self.adapter = TypeAdapter(UpdateRequestBody[file_coord.obj_type])

    async def post(self) -> ResponseReturnValue:
        try:
            body = self.adapter.validate_json(await request.get_data())
            self.file_coord.update(body.id, body.data)
            return asdict(UpdateOkResponse())

        except ValidationError as err:
            return asdict(ParseErrResponse(str(err))), 400

        except FileIdNotFoundError as err:
            return asdict(InvalidIdErrResponse(str(err))), 400

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500


###
### File Blueprint
###


def create_file_blueprint(file_manager: INetworkFileManager, file_coordinator: FileCoordinator) -> Blueprint:
    file_api_name = file_manager.api_name()
    obj_api_name = file_coordinator.api_name

    bp = Blueprint(f"{file_api_name}_files", __name__)

    bp.add_url_rule(
        "/available",
        view_func=AvailableFilesView.as_view(f"available", file_manager),
    )
    bp.add_url_rule(
        "/load",
        view_func=LoadFileView.as_view(f"load", file_manager),
    )
    bp.add_url_rule(
        "/update",
        view_func=UpdateFileView.as_view(f"update", file_manager, file_coordinator),
    )

    return bp


###
### Update File View
###


@dataclass
class UpdateRequestBody(Generic[T]):
    id: FileId
    data: T


@dataclass
class UpdateOkResponse:
    success: Literal[True] = True


class UpdateFileView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: INetworkFileManager[T], file_coord: FileCoordinator):
        self.file_mngr = file_mngr
        self.file_coord = file_coord
        self.adapter = TypeAdapter(UpdateRequestBody[file_mngr.file_type()])

    async def post(self) -> ResponseReturnValue:
        try:
            body = self.adapter.validate_json(await request.get_data())
            self.file_mngr.save_to(body.id, body.data)
            self.file_coord.increment_version(body.id)
            return asdict(UpdateOkResponse())

        except ValidationError as err:
            return asdict(ParseErrResponse(str(err))), 400

        except FileIdNotFoundError as err:
            return asdict(InvalidIdErrResponse(str(err))), 400

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500


###
### Available Files View
###


@dataclass
class AvailableFilesOkResponse(Generic[T]):
    available: list[FileId]
    success: Literal[True] = True


class AvailableFilesView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: INetworkFileManager[T]):
        self.file_mngr = file_mngr

    async def get(self) -> ResponseReturnValue:
        try:
            return asdict(AvailableFilesOkResponse(self.file_mngr.available()))

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500


###
### Load File View
###


@dataclass
class LoadRequestArgs:
    id: FileId


@dataclass
class LoadOkResponse(Generic[T]):
    data: T
    success: Literal[True] = True


class LoadFileView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: INetworkFileManager[T]):
        self.file_mngr = file_mngr
        self.adapter = TypeAdapter(LoadRequestArgs)

    async def get(self) -> ResponseReturnValue:
        try:
            args = self.adapter.validate_python(request.args.to_dict())
            return asdict(LoadOkResponse(self.file_mngr.load(args.id)))

        except ValidationError as err:
            return asdict(ParseErrResponse(str(err))), 400

        except FileIdNotFoundError as err:
            return asdict(InvalidIdErrResponse(str(err))), 400

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500
