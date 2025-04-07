import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
from server.architecture.config import ArchitectureConfig
from server.architecture.service import ArchitectureService
from server.data.service import DataService
from server.layer.service import LayerService
from server.model.loss import default_loss_fns
from server.model.loss.definition import LossDefinition
from server.model.model import ArchitectureModel
from server.model.optim import default_optimizers
from server.model.optim.definition import OptimizerDefinition
from server.model.train import (
    TrainingConfig,
    TrainingInfo,
    TrainingQueuedInfo,
    TrainLogObject,
    get_time,
    training_thread,
)
from server.util.file import (
    JsonFileManager,
    Loadable,
    MetaData,
    TorchWeightsFileManager,
)
from server.util.file.coordinator import FileCoordinator, IdGeneration
from server.util.file.file import FileId
from server.util.registry import Registry


@dataclass
class ModelObject(Loadable):
    meta: MetaData
    data: dict[str, Any]  # the model's state_dict
    architecture: ArchitectureConfig


class ModelService:
    """
    A service for managing PyTorch models.
    """

    training_queue: asyncio.Queue[tuple[FileId, TrainingConfig]]

    def __init__(
        self,
        layer_service: LayerService,
        data_service: DataService,
        architecture_service: ArchitectureService,
        model_save_path: Path,
        training_save_path: Path,
    ) -> None:
        self.loss_fns = Registry[LossDefinition](default_loss_fns)
        self.optimizers = Registry[OptimizerDefinition](default_optimizers)

        self.layer_service = layer_service
        self.data_service = data_service
        self.architecture_service = architecture_service

        self.models = FileCoordinator(
            ModelObject,
            "model",
            TorchWeightsFileManager("data", model_save_path, ".pt"),
            [JsonFileManager("architecture", model_save_path, ArchitectureConfig, ".arch.json")],
            model_save_path,
        )

        self.train_logs = FileCoordinator(
            TrainLogObject,
            "train",
            JsonFileManager("data", training_save_path, TrainingInfo, ".train.log"),  # type: ignore # TODO: fix type error?
            [JsonFileManager("config", training_save_path, TrainingConfig, ".train.cfg")],
            training_save_path,
            IdGeneration.TimeStamp,
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

    def load_model(self, id: FileId):
        model_obj = self.models.get(id)
        model = ArchitectureModel.create_from_architecture(
            model_obj.content.architecture,
            self.layer_service,
        )
        model.load_state_dict(model_obj.content.data)
        return model

    async def add_to_training_queue(self, cfg: TrainingConfig, meta: MetaData) -> FileId:
        log_id = self.train_logs.create(TrainLogObject(meta, TrainingQueuedInfo(get_time()), cfg))
        await self.training_queue.put((log_id, cfg))
        return log_id

    def available_devices(self) -> list[str]:
        devices = ["cpu"]
        if torch.cuda.is_available():
            devices += [f"cuda:{i}" for i in range(torch.cuda.device_count())]
        return devices
