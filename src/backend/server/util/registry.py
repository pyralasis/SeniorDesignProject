from typing import Generic, Protocol, TypeVar


class Registerable(Protocol):
    id: str


TVal = TypeVar("TVal", bound=Registerable)


class Registry(Generic[TVal]):
    _available: dict[str, TVal]

    def __init__(self, layers: list[TVal]) -> None:
        self._available = {}

        for layer in layers:
            self.add(layer)

    def add(self, layer: TVal):
        self._available[layer.id] = layer

    def available(self) -> list[TVal]:
        return list(self._available.values())

    def contains(self, id: str) -> bool:
        return id in self._available

    def get(self, id: str) -> TVal:
        return self._available[id]
