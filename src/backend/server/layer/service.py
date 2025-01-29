from server.layer import LayerDefinition
from server.util.registry import Registry


class LayerService:
    """
    A service for managing layout configurations and files.
    """

    layers: Registry[LayerDefinition]

    def __init__(self, default_layers: list[LayerDefinition]) -> None:
        self.layers = Registry[LayerDefinition](default_layers)
