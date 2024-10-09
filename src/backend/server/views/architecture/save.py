from dataclasses import asdict, dataclass
from typing import Literal
from pydantic import TypeAdapter
from quart import request, ResponseReturnValue
from quart.views import MethodView

from server.architecture.desc import ArchitectureDescription
from server.architecture.service import ArchitectureService


@dataclass
class SaveRequestBody:
    file_name: str
    architecture: ArchitectureDescription


@dataclass
class SuccessfulResponse:
    success: Literal[True] = True


@dataclass
class FailedResponse:
    msg: str
    success: Literal[False] = False


class SaveArchitectureView(MethodView):
    init_every_request = False

    def __init__(self, arch_service: ArchitectureService):
        self.arch_service = arch_service
        self.adapter = TypeAdapter(SaveRequestBody)

    async def post(self) -> ResponseReturnValue:
        body = self.adapter.validate_python(request.json)
        try:
            self.arch_service.save_architecture(body.file_name, body.architecture)
            return asdict(SuccessfulResponse())
        except Exception as error:
            return asdict(FailedResponse(str(error))), 400
