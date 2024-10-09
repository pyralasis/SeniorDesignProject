from dataclasses import asdict, dataclass
from typing import Literal
from pydantic import TypeAdapter
from quart import request, ResponseReturnValue
from quart.views import MethodView

from server import architecture
from server.architecture.loaded import LoadedArchitecture
from server.architecture.service import ArchitectureService


@dataclass
class LoadRequestArgs:
    file_name: str


@dataclass
class SuccessfulResponse:
    architecture: LoadedArchitecture
    success: Literal[True] = True


@dataclass
class FailedResponse:
    msg: str
    success: Literal[False] = False


class LoadArchitectureView(MethodView):
    init_every_request = False

    def __init__(self, arch_service: ArchitectureService):
        self.arch_service = arch_service
        self.adapter = TypeAdapter(LoadRequestArgs)

    async def get(self) -> ResponseReturnValue:
        args = self.adapter.validate_python(request.args)
        try:
            return asdict(
                SuccessfulResponse(self.arch_service.load_architecture(args.file_name))
            )
        except Exception as error:
            return asdict(FailedResponse(str(error))), 400
