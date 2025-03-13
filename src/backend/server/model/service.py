import uuid
from ast import Mod
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.sax import xmlreader

import torch
from server import layer
from server.architecture.config import (
    ArchitectureConfig,
    InputLayerConfig,
    LayerInstanceID,
    NetworkLayerConfig,
)
from server.layer import LayerDefinition
from server.layer.service import LayerService
from server.layer.size import TensorSize
from server.model.model import ArchitectureModel
from server.util.file import Loadable, MetaData, TorchWeightsFileManager
from server.util.file.coordinator import FileCoordinator
from server.util.file.file import FileId

"""
Sample model architecture:
{
    "name": "Example Architecture",
    "version": 1,
    "inputs": [{"id":1,"size":[10]}],
    "layers": [
        {"id":2,"layer_id":"linear","input":1,"param_values":{"out_features":{"val":5,"type":"int"},"bias":{"val":true,"type":"bool"}}},
        {"id":3,"layer_id":"linear","input":2,"param_values":{"out_features":{"val":1,"type":"int"},"bias":{"val":true,"type":"bool"}}}
    ],
    "layout_file": null
}
"""


@dataclass
class ModelObject(Loadable):
    meta: MetaData
    data: dict[str, Any]  # the model's state_dict


class ModelService:
    """
    A service for managing PyTorch models.
    """

    def __init__(self, layer_service: LayerService, save_path: Path) -> None:
        self.layer_service = layer_service
        self.models = FileCoordinator(
            ModelObject,
            "model",
            TorchWeightsFileManager("data", save_path, ".pt"),
            [],
            save_path,
        )

    def create_model(self, architecture: ArchitectureConfig, meta_data: MetaData) -> FileId:
        model = ArchitectureModel.create_from_architecture(architecture, self.layer_service)
        model_id = self.models.create(ModelObject(meta_data, model.state_dict()))  # save the model to the file system
        return model_id
