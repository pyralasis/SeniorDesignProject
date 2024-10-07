from quart import Blueprint

from server.architecture.service import ArchitectureService

def create_architecture_blueprint(architecture_service: ArchitectureService) -> Blueprint:
    bp = Blueprint('architecture', __name__)

    return bp