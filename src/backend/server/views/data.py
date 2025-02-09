from quart import Blueprint
from quart.views import MethodView
from server.data.service import DataService
from server.data.sources.base import DataSourceDescription
from server.data.transforms.base import TransformDescription
from server.util.file import create_object_blueprint


def create_data_blueprint(
    data_service: DataService,
) -> Blueprint:
    bp = Blueprint("data", __name__)

    bp.add_url_rule(
        "/available_sources",
        view_func=AvailableSourcesView.as_view("available_sources", data_service),
    )
    bp.add_url_rule(
        "/available_transforms",
        view_func=AvailableTransformsView.as_view("available_transforms", data_service),
    )

    bp.register_blueprint(create_object_blueprint(data_service.pipelines))

    return bp


###
### Available Transforms View
###

AvailableTransformsResponse = list[TransformDescription]


class AvailableTransformsView(MethodView):
    init_every_request = False

    def __init__(self, data_service: DataService):
        self.data_service = data_service

    async def get(self) -> AvailableTransformsResponse:
        available_transforms = self.data_service.transforms.available()
        descriptions: AvailableTransformsResponse = list(
            map(lambda transform: transform.description(), available_transforms)
        )
        return descriptions


###
### Available Sources View
###

AvailableSourcesResponse = list[DataSourceDescription]


class AvailableSourcesView(MethodView):
    init_every_request = False

    def __init__(self, data_service: DataService):
        self.data_service = data_service

    async def get(self):
        available_transforms = self.data_service.sources.available()
        descriptions: AvailableSourcesResponse = list(
            map(lambda transform: transform.description(), available_transforms)
        )
        return descriptions
