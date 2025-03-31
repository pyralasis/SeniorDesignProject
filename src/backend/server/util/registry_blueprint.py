from dataclasses import asdict, dataclass
from typing import Any, Generic, Literal, Protocol, TypeVar

from pydantic import TypeAdapter, ValidationError
from quart import Blueprint, ResponseReturnValue, request
from quart.views import MethodView
from server.util.errors import InvalidRequestErrResponse
from server.util.registry import Registry

TDesc = TypeVar("TDesc", covariant=True)


class RegisterableDefinition(Protocol, Generic[TDesc]):
    id: str

    def description(self) -> TDesc: ...


TVal = TypeVar("TVal", bound=RegisterableDefinition)


def create_registry_blueprint(registry: Registry[TVal], registry_item: str):
    bp = Blueprint(registry_item, __name__)

    bp.add_url_rule(
        "/available",
        view_func=AvailableItemsView[TVal].as_view("available", registry),
    )
    bp.add_url_rule(
        "/get",
        view_func=GetLayerView[TVal].as_view("get", registry),
    )

    return bp


###
### General Errors
###


@dataclass
class InvalidItemErrResponse:
    msg: str
    success: Literal[False] = False
    error_type: Literal["invalid_item"] = "invalid_item"


###
### Available ITems
###


AvailableLayersResponse = list[TDesc]


class AvailableItemsView(MethodView, Generic[TVal]):
    init_every_request = False

    def __init__(self, registry: Registry[TVal]):
        self.registry = registry

    async def get(self) -> ResponseReturnValue:
        available_definitions = self.registry.available()
        descriptions: AvailableLayersResponse = list(
            map(lambda item_def: item_def.description(), available_definitions)
        )
        return descriptions


###
### Get Item View
###


@dataclass
class GetItemArgs:
    id: str


@dataclass
class GetItemOkResponse(Generic[TDesc]):
    layer: TDesc
    success: Literal[True] = True


class GetLayerView(MethodView, Generic[TVal]):
    init_every_request = False

    def __init__(self, registry: Registry[TVal]):
        self.registry = registry
        self.adapter = TypeAdapter(GetItemArgs)

    async def get(self) -> ResponseReturnValue:
        try:
            args = self.adapter.validate_python(request.args.to_dict())
            if self.registry.contains(args.id):
                return asdict(GetItemOkResponse(self.registry.get(args.id).description()))
            else:
                return asdict(InvalidItemErrResponse(f"No item found with id '{args.id}'")), 400

        except ValidationError as err:
            return asdict(InvalidRequestErrResponse(str(err))), 400
