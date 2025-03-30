import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch.multiprocessing as mp
from server.architecture.config import ArchitectureConfig
from server.architecture.service import ArchitectureService
from server.data.service import DataService
from server.data.sources.base import DataSourceDataset
from server.layer.service import LayerService
from server.model.loss import default_loss_fns
from server.model.loss.definition import LossDefinition
from server.model.model import ArchitectureModel
from server.model.optim import default_optimizers
from server.model.optim.definition import OptimizerDefinition
from server.model.train import TrainingConfig, training_thread
from server.util.file import (
    JsonFileManager,
    Loadable,
    MetaData,
    TorchWeightsFileManager,
)
from server.util.file.coordinator import FileCoordinator
from server.util.file.file import FileId
from server.util.registry import Registry
from torch import Tensor, nn, optim
from torch.nn import NLLLoss
from torch.optim import Adam
from torch.utils.data import DataLoader

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
    architecture: ArchitectureConfig


class ModelService:
    """
    A service for managing PyTorch models.
    """

    training_queue: asyncio.Queue[TrainingConfig]

    def __init__(
        self,
        layer_service: LayerService,
        data_service: DataService,
        architecture_service: ArchitectureService,
        save_path: Path,
    ) -> None:
        self.loss_fns = Registry[LossDefinition](default_loss_fns)
        self.optimizers = Registry[OptimizerDefinition](default_optimizers)

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

        self.training_queue = asyncio.Queue()

    async def start_training_task(self):
        self.training_task = asyncio.create_task(training_thread(self))

    def create_model(self, architecture: ArchitectureConfig, meta_data: MetaData) -> FileId:
        model = ArchitectureModel.create_from_architecture(architecture, self.layer_service)
        model_id = self.models.create(
            ModelObject(meta_data, model.state_dict(), architecture)
        )  # save the model to the file system

        return model_id

    async def add_to_training_queue(self, cfg: TrainingConfig):
        await self.training_queue.put(cfg)
