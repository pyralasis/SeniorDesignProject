from quart import Blueprint

from server.layer import LayerDefinition
from server.util.registry import Registry
from server.views.layers.available import AvailableLayersView
from server.views.layers.output_size import LayerOutputSizeView


def create_layer_blueprint(layer_registry: Registry[LayerDefinition]) -> Blueprint:
    bp = Blueprint("layer", __name__)

    bp.add_url_rule(
        "/available",
        view_func=AvailableLayersView.as_view("available_layers", layer_registry),
    )
    bp.add_url_rule(
        "/output_size",
        view_func=LayerOutputSizeView.as_view("output_size", layer_registry),
    )

    return bp
