from quart import ResponseReturnValue
from quart.views import MethodView

from server.model.service import ModelService


class CreateModelView(MethodView):
    init_every_request = False

    def __init__(self, model_service: ModelService):
        self.service = model_service

    async def post(self) -> ResponseReturnValue:
        return "Model Post Hello World!"
