
from abc import ABC, abstractmethod
from typing import Any
from quart import ResponseReturnValue, current_app
from quart.views import View

class WebsocketView(View, ABC):
    """A Websocket specific view class.
    """

    async def dispatch_request(self, **kwargs: Any) -> ResponseReturnValue:
        handler = getattr(self, "ws", None)
        return await current_app.ensure_async(handler)(**kwargs) # type: ignore
