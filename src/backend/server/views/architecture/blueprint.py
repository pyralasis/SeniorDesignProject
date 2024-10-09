from quart import Blueprint

from server.architecture.service import ArchitectureService
from server.views.architecture.available import AvailableArchitecturesView
from server.views.architecture.delete import DeleteArchitectureView
from server.views.architecture.load import LoadArchitectureView
from server.views.architecture.save import SaveArchitectureView


def create_architecture_blueprint(
    architecture_service: ArchitectureService,
) -> Blueprint:
    bp = Blueprint("architecture", __name__)

    bp.add_url_rule(
        "/available",
        view_func=AvailableArchitecturesView.as_view(
            "available_architectures", architecture_service
        ),
    )
    bp.add_url_rule(
        "/delete",
        view_func=DeleteArchitectureView.as_view(
            "delete_architecture", architecture_service
        ),
    )
    bp.add_url_rule(
        "/load",
        view_func=LoadArchitectureView.as_view(
            "load_architecture", architecture_service
        ),
    )
    bp.add_url_rule(
        "/save",
        view_func=SaveArchitectureView.as_view(
            "save_architecture", architecture_service
        ),
    )

    return bp
