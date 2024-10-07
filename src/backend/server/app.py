from quart import Quart

from server.architecture.service import ArchitectureService
from server.layer.definitions import default_layers
from server.layer.registry import LayerRegistry
from server.views.blueprint import create_api_blueprint


def create_app():
    app = Quart(__name__)

    layer_registry = LayerRegistry(default_layers)
    architecture_service = ArchitectureService()

    app.register_blueprint(create_api_blueprint(architecture_service, layer_registry), url_prefix="/api")

    return app


# Create subclass of Quart App?
