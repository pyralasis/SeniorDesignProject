from dataclasses import asdict, dataclass
from typing import Generic, Literal, TypeVar
from pydantic import TypeAdapter, ValidationError
from quart import Blueprint, ResponseReturnValue, request
from quart.views import MethodView

from server.util.file.loaded import Loaded
from server.util.file.manager import BaseFileManager, FileIdNotFoundError, InvalidFileFormatError, JsonFileManager
from server.util.file.id import FileId


def create_file_blueprint(file_manager: BaseFileManager, file_type_name: str) -> Blueprint:
    bp = Blueprint(f"{file_type_name}_files", __name__)

    bp.add_url_rule(
        "/available",
        view_func=AvailableFilesView.as_view(f"available_{file_type_name}", file_manager),
    )
    bp.add_url_rule(
        "/delete",
        view_func=DeleteFileView.as_view(f"delete_{file_type_name}", file_manager),
    )
    bp.add_url_rule(
        "/load",
        view_func=LoadFileView.as_view(f"load_{file_type_name}", file_manager),
    )
    bp.add_url_rule(
        "/create",
        view_func=CreateFileView.as_view(f"create_{file_type_name}", file_manager),
    )
    bp.add_url_rule(
        "/update",
        view_func=UpdateFileView.as_view(f"update_{file_type_name}", file_manager),
    )

    return bp


###
### General
###

T = TypeVar("T")


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
### Create File View
###


@dataclass
class CreateRequestBody(Generic[T]):
    data: T


@dataclass
class CreateOkResponse:
    success: Literal[True] = True


class CreateFileView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: JsonFileManager[T]):
        self.file_mngr = file_mngr
        self.adapter = TypeAdapter(CreateRequestBody[file_mngr.file_type])

    async def post(self) -> ResponseReturnValue:
        try:
            # Uses validate_json and request.get_data() instead of validate_python and request.json
            # for better/easier validation
            body = self.adapter.validate_json(await request.get_data())
            self.file_mngr.create(body.data)
            return asdict(CreateOkResponse())

        except ValidationError as err:
            return asdict(ParseErrResponse(str(err))), 400

        except FileIdNotFoundError as err:
            return asdict(InvalidIdErrResponse(str(err))), 400

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500


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

    def __init__(self, file_mngr: JsonFileManager[T]):
        self.file_mngr = file_mngr
        self.adapter = TypeAdapter(UpdateRequestBody[file_mngr.file_type])

    async def post(self) -> ResponseReturnValue:
        try:
            body = self.adapter.validate_json(await request.get_data())
            self.file_mngr.update(body.id, body.data)
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
class AvailableOkResponse(Generic[T]):
    available: list[FileId]
    success: Literal[True] = True


class AvailableFilesView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: BaseFileManager[T]):
        self.file_mngr = file_mngr

    async def get(self) -> ResponseReturnValue:
        try:
            return asdict(AvailableOkResponse(self.file_mngr.available()))

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
    data: Loaded[T]
    success: Literal[True] = True


class LoadFileView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: BaseFileManager[T]):
        self.file_mngr = file_mngr
        self.adapter = TypeAdapter(LoadRequestArgs)

    async def get(self) -> ResponseReturnValue:
        try:
            args = self.adapter.validate_python(request.args)
            return asdict(LoadOkResponse(self.file_mngr.load(args.id)))

        except ValidationError as err:
            return asdict(ParseErrResponse(str(err))), 400

        except FileIdNotFoundError as err:
            return asdict(InvalidIdErrResponse(str(err))), 400

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500


###
### Delete File View
###


@dataclass
class DeleteRequestBody:
    id: FileId


@dataclass
class DeleteOkResponse:
    success: Literal[True] = True


class DeleteFileView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: BaseFileManager[T]):
        self.file_mngr = file_mngr
        self.adapter = TypeAdapter(DeleteRequestBody)

    async def post(self) -> ResponseReturnValue:
        try:
            body = self.adapter.validate_json(await request.get_data())
            self.file_mngr.delete(body.id)
            return asdict(DeleteOkResponse())

        except ValidationError as err:
            return asdict(ParseErrResponse(str(err))), 400

        except FileIdNotFoundError as err:
            return asdict(InvalidIdErrResponse(str(err))), 400

        except (IOError, InvalidFileFormatError) as err:
            return asdict(IOErrResponse(str(err))), 500
