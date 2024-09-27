
from quart.views import MethodView


class TestView(MethodView):
    init_every_request = False

    def __init__(self, msg: str):
        self.msg = msg

    async def get(self):
        return self.msg
