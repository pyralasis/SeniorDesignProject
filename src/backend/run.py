
from server.app import create_app


if __name__ == "__main__":
    app = create_app()

    app.run("0.0.0.0", 7777, debug=True)
