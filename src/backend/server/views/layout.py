from quart import Blueprint

from server.layout.service import LayoutService
from server.util.file.blueprint import create_file_blueprint


def create_layout_blueprint(
    layout_service: LayoutService,
) -> Blueprint:
    bp = Blueprint("layout", __name__)

    bp.register_blueprint(create_file_blueprint(layout_service.files, "layout"))

    return bp
