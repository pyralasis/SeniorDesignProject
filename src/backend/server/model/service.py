from server.architecture.service import ArchitectureService
from server.layer import LayerDefinition
from server.layer.service import LayerService
from server.util.registry import Registry


class ModelService:
    """
    A service for managing PyTorch models.
    """

    def __init__(self, layer_service: LayerService, architecture_service: ArchitectureService) -> None:
        self.layer_service = layer_service
        self.architecture_service = architecture_service

    def create_model(self) -> None:
        # Stub
        ...
