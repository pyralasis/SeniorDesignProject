from quart import Blueprint

from server.views.architecture.blueprint import create_architecture_blueprint
from server.views.data.blueprint import create_data_blueprint
from server.views.model.blueprint import create_model_blueprint
from server.views.test import TestView
from server.views.test_ws import TestWebsocketView


def create_api_blueprint() -> Blueprint:
    bp = Blueprint('api', __name__)

    bp.add_url_rule("/test", view_func=TestView.as_view("test", "Hello World!"))
    bp.add_websocket("/test_ws", view_func=TestWebsocketView.as_view("test_ws", "Hello World!"))

    bp.register_blueprint(create_architecture_blueprint(), url_prefix="/architecture")
    bp.register_blueprint(create_data_blueprint(), url_prefix="/data")
    bp.register_blueprint(create_model_blueprint(), url_prefix="/model")

    return bp