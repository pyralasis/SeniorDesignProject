from quart import Blueprint

def create_data_blueprint() -> Blueprint:
    bp = Blueprint('data', __name__)

    return bp