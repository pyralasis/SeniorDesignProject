from dataclasses import asdict, dataclass
from typing import Generic, Literal, TypeVar
from pydantic import TypeAdapter
from quart import ResponseReturnValue, request
from quart.views import MethodView

from server.architecture.config import ArchitectureConfig
from server.architecture.service import ArchitectureService
from server.util.file.manager import BaseFileManager

T = TypeVar("T")


@dataclass
class DeleteRequestBody:
    file_name: str


@dataclass
class SuccessfulResponse:
    success: Literal[True] = True


@dataclass
class FailedResponse:
    msg: str
    success: Literal[False] = False


class DeleteFileView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: BaseFileManager[T]):
        self.file_mngr = file_mngr
        self.adapter = TypeAdapter(DeleteRequestBody)

    async def post(self) -> ResponseReturnValue:
        body = self.adapter.validate_python(request.json)
        try:
            self.file_mngr.delete(body.file_name)
            return asdict(SuccessfulResponse())
        except Exception as error:
            return asdict(FailedResponse(str(error))), 400
