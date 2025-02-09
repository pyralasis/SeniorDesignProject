from quart import Blueprint
from server.architecture.service import ArchitectureService
from server.util.file import create_object_blueprint


def create_architecture_blueprint(
    architecture_service: ArchitectureService,
) -> Blueprint:
    bp = Blueprint("architecture", __name__)

    # this collectively adds file management endpoints for the architecture service
    bp.register_blueprint(create_object_blueprint(architecture_service.architectures))

    return bp
