from server.architecture.service import ArchitectureService
from server.util.file.blueprint import create_file_blueprint


from quart import Blueprint


def create_architecture_blueprint(
    architecture_service: ArchitectureService,
) -> Blueprint:
    bp = Blueprint("architecture", __name__)

    # this collectively adds file management endpoints for the architecture service
    bp.register_blueprint(create_file_blueprint(architecture_service.files, "architecture"))

    return bp
