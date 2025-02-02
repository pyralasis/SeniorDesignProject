from pathlib import Path
from quart import Quart

from server.architecture.service import ArchitectureService
from server.data.service import DataService
from server.data.sources import default_sources
from server.data.transforms import default_transforms
from server.layer.definitions import default_layers
from server.layer.service import LayerService
from server.layout.service import LayoutService
from server.model.service import ModelService
from server.views.blueprint import create_api_blueprint

DEFAULT_PATHS = {
    "architectures": "./architectures",
    "models": "./models",
    "layouts": "./layouts",
    "data": "./data",
}

def create_app():
    app = Quart(__name__)

    layer_service = LayerService(default_layers)
    architecture_service = ArchitectureService(Path(DEFAULT_PATHS["architectures"]))
    data_service = DataService(Path(DEFAULT_PATHS["data"]), default_sources, default_transforms)
    layout_service = LayoutService(Path(DEFAULT_PATHS["layouts"]))
    model_service = ModelService(layer_service, Path(DEFAULT_PATHS["models"]))

    # These are where the API endpoints are registered
    app.register_blueprint(
        create_api_blueprint(architecture_service, layer_service, data_service, layout_service, model_service), url_prefix="/api"
    )

    return app


# Create subclass of Quart App?
