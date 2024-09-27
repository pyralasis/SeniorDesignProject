from quart import websocket
from server.util.override_decorator import override
from server.util.websocket_view import WebsocketView


class TestWebsocketView(WebsocketView):
    init_every_request = False

    def __init__(self, msg: str):
        self.msg = msg

    async def ws(self):
        await websocket.send_json({
            "msg": self.msg,
        })
