from dataclasses import asdict, dataclass
from typing import Generic, Literal, TypeVar
from quart import ResponseReturnValue
from quart.views import MethodView

from server.util.file.loaded import Loaded
from server.util.file.manager import BaseFileManager

T = TypeVar("T")


@dataclass
class SuccessfulResponse(Generic[T]):
    available: list[Loaded[T]]
    success: Literal[True] = True


class AvailableFilesView(MethodView, Generic[T]):
    init_every_request = False

    def __init__(self, file_mngr: BaseFileManager[T]):
        self.file_mngr = file_mngr

    async def get(self) -> ResponseReturnValue:
        return asdict(SuccessfulResponse(self.file_mngr.load_all()))
