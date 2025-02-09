import os

from quart_cors import cors
from server.app import create_app
from server.util.tools import get_routes, print_routes

if __name__ == "__main__":
    app = cors(create_app())

    if True:
        print_routes(app)

    print("Starting server on port 7777")
    app.run("0.0.0.0", 7777, debug=True)
