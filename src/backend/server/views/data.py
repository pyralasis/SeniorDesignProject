from quart import Blueprint
from server.data.service import DataService
from server.util.file import create_object_blueprint
from server.util.registry_blueprint import create_registry_blueprint


def create_data_blueprint(
    data_service: DataService,
) -> Blueprint:
    bp = Blueprint("data", __name__)

    bp.register_blueprint(create_registry_blueprint(data_service.sources, "source"), url_prefix="/source")
    bp.register_blueprint(create_registry_blueprint(data_service.transforms, "transform"), url_prefix="/transform")

    bp.register_blueprint(create_object_blueprint(data_service.pipelines))

    return bp
