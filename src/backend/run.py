from quart_cors import cors
from server.app import create_app


if __name__ == "__main__":
    app = cors(create_app())

    app.run("0.0.0.0", 7777, debug=True)
