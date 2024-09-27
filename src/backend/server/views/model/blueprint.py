from quart import Blueprint

def create_model_blueprint() -> Blueprint:
    bp = Blueprint('model', __name__)

    return bp