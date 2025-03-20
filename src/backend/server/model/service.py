import uuid
from ast import Mod
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.sax import xmlreader

import torch
from torch.optim import Adam
from torch.nn import MSELoss
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
from server.data.service import DataService
from server.architecture.service import ArchitectureService
from server.util.file import JsonFileManager

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
class TrainingConfig:
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 10


@dataclass
class ModelObject(Loadable):
    meta: MetaData
    data: dict[str, Any]  # the model's state_dict
    architecture: ArchitectureConfig

class ModelService:
    """
    A service for managing PyTorch models.
    """

    def __init__(
        self,
        layer_service: LayerService,
        data_service: DataService,
        architecture_service: ArchitectureService,
        save_path: Path,
    ) -> None:
        self.layer_service = layer_service
        self.data_service = data_service
        self.architecture_service = architecture_service
        self.models = FileCoordinator(
            ModelObject,
            "model",
            TorchWeightsFileManager("data", save_path, ".pt"),
            [JsonFileManager("architecture", save_path, ArchitectureConfig, ".arch.json")],
            save_path,
        )

    def create_model(
        self, architecture: ArchitectureConfig, meta_data: MetaData
    ) -> FileId:
        model = ArchitectureModel.create_from_architecture(
            architecture, self.layer_service
        )
        model_id = self.models.create(
            ModelObject(meta_data, model.state_dict(), architecture)
        )  # save the model to the file system

        return model_id

    def train_model(
        self,
        model_id: FileId,
        source_id: FileId,
        config: TrainingConfig = TrainingConfig(),
    ) -> None:
        """
        Train a model using the specified data source and training configuration.

        Args:
            model_id: ID of the model to train
            source_id: ID of the data source to use for training
            config: Training configuration parameters
        """
        # Load the model
        model_obj = self.models.get(model_id)
        model = ArchitectureModel.create_from_architecture(
            model_obj.architecture,
            self.layer_service,
        )
        model.load_state_dict(model_obj.data)

        # Load the data
        value_source, label_source = self.data_service.config_to_sources(
            self.data_service.pipelines.get(source_id).data
        )

        # Setup training
        optimizer = Adam(model.parameters(), lr=config.learning_rate)
        criterion = MSELoss()

        # Training loop
        model.train()
        for epoch in range(config.epochs):
            for i in range(0, len(value_source), config.batch_size):
                batch_inputs = [
                    value_source[j]
                    for j in range(i, min(i + config.batch_size, len(value_source)))
                ]
                batch_labels = [
                    label_source[j]
                    for j in range(i, min(i + config.batch_size, len(label_source)))
                ]

                # Convert to tensors
                inputs = torch.stack(batch_inputs)
                labels = torch.stack(batch_labels)

                # Forward pass
                outputs = model(inputs)
                loss = criterion(outputs, labels)

                # Backward pass and optimize
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        # Save the updated model
        self.models.update(
            model_id, ModelObject(model_obj.meta, model.state_dict(), model_obj.architecture)
        )
