from dataclasses import asdict, dataclass
from typing import Literal
from pydantic import TypeAdapter
from quart import ResponseReturnValue, request
from quart.views import MethodView

from server.architecture.desc import ArchitectureDescription
from server.architecture.service import ArchitectureService


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


class DeleteArchitectureView(MethodView):
    init_every_request = False

    def __init__(self, arch_service: ArchitectureService):
        self.arch_service = arch_service
        self.adapter = TypeAdapter(DeleteRequestBody)

    async def post(self) -> ResponseReturnValue:
        body = self.adapter.validate_python(request.json)
        try:
            self.arch_service.delete_architecture(body.file_name)
            return asdict(SuccessfulResponse())
        except Exception as error:
            return asdict(FailedResponse(str(error))), 400
