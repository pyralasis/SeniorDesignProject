from pathlib import Path
from quart import Quart

from server.architecture.service import ArchitectureService
from server.data.service import DataService
from server.data.sources import default_sources
from server.data.transforms import default_transforms
from server.layer import LayerDefinition
from server.layer.definitions import default_layers
from server.util.registry import Registry
from server.views.blueprint import create_api_blueprint


def create_app():
    app = Quart(__name__)

    layer_registry = Registry[LayerDefinition](default_layers)
    architecture_service = ArchitectureService(Path("./architectures"))
    data_service = DataService(Path("./pipelines"), default_sources, default_transforms)

    app.register_blueprint(create_api_blueprint(architecture_service, layer_registry, data_service), url_prefix="/api")

    return app


# Create subclass of Quart App?
