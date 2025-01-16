from dataclasses import asdict, dataclass
from typing import Generic, Literal, TypeVar
from pydantic import TypeAdapter
from quart import request, ResponseReturnValue
from quart.views import MethodView

from server.architecture.config import ArchitectureConfig
from server.architecture.service import ArchitectureService
from server.util.file.manager import FileManager


T = TypeVar("T")


@dataclass
class SaveRequestBody(Generic[T]):
    file_name: str
    data: T


@dataclass
class SuccessfulResponse:
    success: Literal[True] = True


@dataclass
class FailedResponse:
    msg: str
    success: Literal[False] = False


class SaveFileView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: FileManager[T]):
        self.file_mngr = file_mngr
        self.adapter = TypeAdapter(SaveRequestBody[file_mngr.file_type])

    async def post(self) -> ResponseReturnValue:
        body = self.adapter.validate_python(request.json)
        try:
            self.file_mngr.save(body.file_name, body.data)
            return asdict(SuccessfulResponse())
        except Exception as error:
            return asdict(FailedResponse(str(error))), 400
