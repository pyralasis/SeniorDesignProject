from quart import Blueprint

from server.layer.service import LayerService
from server.views.layers.available import AvailableLayersView
from server.views.layers.output_size import LayerOutputSizeView


def create_layer_blueprint(layer_service: LayerService) -> Blueprint:
    bp = Blueprint("layer", __name__)

    bp.add_url_rule(
        "/available",
        view_func=AvailableLayersView.as_view("available_layers", layer_service),
    )
    bp.add_url_rule(
        "/output_size",
        view_func=LayerOutputSizeView.as_view("output_size", layer_service),
    )

    return bp
