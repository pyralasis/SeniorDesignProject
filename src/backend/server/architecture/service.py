from backend.server.architecture.layers import Layer


class ArchitectureService:
    available_layers: dict[str, Layer]

    def __init__(self) -> None:
        self.available_layers = {}