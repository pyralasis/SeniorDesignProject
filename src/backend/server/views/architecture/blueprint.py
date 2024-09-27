from quart import Blueprint

def create_architecture_blueprint() -> Blueprint:
    bp = Blueprint('architecture', __name__)

    return bp