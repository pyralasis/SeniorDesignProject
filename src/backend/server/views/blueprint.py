from quart import Blueprint

from server.architecture.service import ArchitectureService
from server.data.service import DataService
from server.layer import LayerDefinition
from server.util.registry import Registry
from server.views.architecture.blueprint import create_architecture_blueprint
from server.views.data.blueprint import create_data_blueprint
from server.views.layers.blueprint import create_layer_blueprint
from server.views.model.blueprint import create_model_blueprint
from server.views.test import TestView
from server.views.test_ws import TestWebsocketView


def create_api_blueprint(
    architecture_service: ArchitectureService, layer_registry: Registry[LayerDefinition], data_service: DataService
) -> Blueprint:
    bp = Blueprint("api", __name__)

    bp.add_url_rule("/test", view_func=TestView.as_view("test", "Hello World!"))
    bp.add_websocket("/test_ws", view_func=TestWebsocketView.as_view("test_ws", "Hello World!"))

    bp.register_blueprint(create_architecture_blueprint(architecture_service), url_prefix="/architecture")
    bp.register_blueprint(create_data_blueprint(data_service), url_prefix="/data")
    bp.register_blueprint(create_model_blueprint(), url_prefix="/model")
    bp.register_blueprint(create_layer_blueprint(layer_registry), url_prefix="/layer")

    return bp
