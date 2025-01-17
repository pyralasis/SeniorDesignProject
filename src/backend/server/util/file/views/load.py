from dataclasses import asdict, dataclass
from typing import Generic, Literal, TypeVar
from pydantic import TypeAdapter
from quart import request, ResponseReturnValue
from quart.views import MethodView

from server.util.file.loaded import Loaded
from server.util.file.manager import BaseFileManager


T = TypeVar("T")


@dataclass
class LoadRequestArgs:
    file_name: str


@dataclass
class SuccessfulResponse(Generic[T]):
    data: Loaded[T]
    success: Literal[True] = True


@dataclass
class FailedResponse:
    msg: str
    success: Literal[False] = False


class LoadFileView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: BaseFileManager[T]):
        self.file_mngr = file_mngr
        self.adapter = TypeAdapter(LoadRequestArgs)

    async def get(self) -> ResponseReturnValue:
        args = self.adapter.validate_python(request.args)
        try:
            return asdict(SuccessfulResponse(self.file_mngr.load(args.file_name)))
        except Exception as error:
            return asdict(FailedResponse(str(error))), 400
