from server.architecture.config import ArchitectureConfig
from server.layer.service import LayerService


class ModelService:
    """
    A service for managing PyTorch models.
    """

    def __init__(self, layer_service: LayerService) -> None:
        self.layer_service = layer_service

    # TODO
    # - create the model from the architecture
    # - save the model to the file system
    # - return the model_id
    def create_model(self, architecture: ArchitectureConfig, name: str) -> str:
        # Stub
        return "model_id"
