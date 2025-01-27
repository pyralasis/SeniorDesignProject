from quart import Blueprint
from server.architecture.service import ArchitectureService
from server.model.service import ModelService
from server.views.model.create import CreateModelView

def create_model_blueprint(model_service: ModelService, architecture_service: ArchitectureService) -> Blueprint:
    bp = Blueprint('model', __name__)

    bp.add_url_rule("/create", view_func=CreateModelView.as_view("create_model", model_service, architecture_service))

    return bp
