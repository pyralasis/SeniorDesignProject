from quart import Quart

from server.views.blueprint import create_api_blueprint


def create_app():
    app = Quart(__name__)

    app.register_blueprint(create_api_blueprint(), url_prefix="/api")

    return app


# Create subclass of Quart App?
