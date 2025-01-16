from quart import ResponseReturnValue
from quart.views import MethodView

from server.data.service import DataService
from server.data.sources.base import DataSourceDefinition, DataSourceDescription
from server.util.registry import Registry

Response = list[DataSourceDescription]


class AvailableSourcesView(MethodView):
    init_every_request = False

    def __init__(self, data_service: DataService):
        self.data_service = data_service

    async def get(self) -> ResponseReturnValue:
        available_transforms = self.data_service.sources.available()
        descriptions: Response = list(map(lambda transform: transform.description(), available_transforms))
        return descriptions
