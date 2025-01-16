from quart import ResponseReturnValue
from quart.views import MethodView

from server.data.service import DataService
from server.data.transforms.base import TransformDescription

Response = list[TransformDescription]


class AvailableTransformsView(MethodView):
    init_every_request = False

    def __init__(self, data_service: DataService):
        self.data_service = data_service

    async def get(self) -> ResponseReturnValue:
        available_transforms = self.data_service.transforms.available()
        descriptions: Response = list(map(lambda transform: transform.description(), available_transforms))
        return descriptions
