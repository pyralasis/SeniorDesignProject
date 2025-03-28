import asyncio
import os

from quart_cors import cors
from server.app import create_app
from server.util.tools import get_routes, print_routes


async def main():
    # type:ignore
    app_no_cors = await create_app()
    app = cors(app_no_cors)

    if True:
        print_routes(app)

    print("Starting server on port 7777")
    await app.run_task("0.0.0.0", 7777, debug=True)


if __name__ == "__main__":
    asyncio.run(main())
