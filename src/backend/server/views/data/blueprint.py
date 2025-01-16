from quart import Blueprint

from server.data.service import DataService
from server.util.file.blueprint import create_file_blueprint
from server.views.data.available_sources import AvailableSourcesView
from server.views.data.available_transforms import AvailableTransformsView


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

    bp.register_blueprint(create_file_blueprint(data_service.pipelines, "pipeline"))

    return bp
