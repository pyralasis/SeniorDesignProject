from quart import Blueprint

from server.util.file.manager import BaseFileManager
from server.util.file.views.available import AvailableFilesView
from server.util.file.views.delete import DeleteFileView
from server.util.file.views.load import LoadFileView
from server.util.file.views.save import SaveFileView


def create_file_blueprint(file_manager: BaseFileManager, file_type_name: str) -> Blueprint:
    bp = Blueprint(f"{file_type_name}_files", __name__)

    bp.add_url_rule(
        "/available",
        view_func=AvailableFilesView.as_view(f"available_{file_type_name}", file_manager),
    )
    bp.add_url_rule(
        "/delete",
        view_func=DeleteFileView.as_view(f"delete_{file_type_name}", file_manager),
    )
    bp.add_url_rule(
        "/load",
        view_func=LoadFileView.as_view(f"load_{file_type_name}", file_manager),
    )
    bp.add_url_rule(
        "/save",
        view_func=SaveFileView.as_view(f"save_{file_type_name}", file_manager),
    )

    return bp
