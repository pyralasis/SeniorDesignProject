from dataclasses import asdict, dataclass
from typing import Literal
from quart import ResponseReturnValue
from quart.views import MethodView

from server.architecture.loaded import LoadedArchitecture
from server.architecture.service import ArchitectureService


@dataclass
class SuccessfulResponse:
    architectures: list[LoadedArchitecture]
    success: Literal[True] = True


class AvailableArchitecturesView(MethodView):
    init_every_request = False

    def __init__(self, arch_service: ArchitectureService):
        self.arch_service = arch_service

    async def get(self) -> ResponseReturnValue:
        return asdict(SuccessfulResponse(self.arch_service.load_all_architectures()))
