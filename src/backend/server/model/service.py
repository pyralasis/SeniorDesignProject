import asyncio
import uuid
from ast import Mod
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.sax import xmlreader

import torch
import torch.multiprocessing as mp
from server import layer
from server.architecture.config import (
    ArchitectureConfig,
    InputLayerConfig,
    LayerInstanceID,
    NetworkLayerConfig,
)
from server.architecture.service import ArchitectureService
from server.data.service import DataService
from server.data.sources.base import DataSourceDataset
from server.layer import LayerDefinition
from server.layer.service import LayerService
from server.layer.size import TensorSize
from server.model.model import ArchitectureModel
from server.util.file import (
    JsonFileManager,
    Loadable,
    MetaData,
    TorchWeightsFileManager,
)
from server.util.file.coordinator import FileCoordinator
from server.util.file.file import FileId
from torch import T, Tensor, nn, optim
from torch.nn import MSELoss, NLLLoss
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
class TrainingConfig:
    model_id: FileId
    source_id: FileId
    shuffle_data: bool = True
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

    training_queue: asyncio.Queue[TrainingConfig]

    async def __init__(
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

        self.training_queue = asyncio.Queue()
        self.training_task = asyncio.create_task(self.training_thread())

    async def training_thread(self):
        await asyncio.sleep(0.01)
        print("RUNNING")
        while True:
            cfg = await self.training_queue.get()
            msg_queue = mp.Queue()

            # Load the model
            model_obj = self.models.get(cfg.model_id)
            model = ArchitectureModel.create_from_architecture(
                model_obj.content.architecture,
                self.layer_service,
            )
            model.load_state_dict(model_obj.content.data)

            # Load the data
            value_source, label_source = self.data_service.config_to_sources(
                self.data_service.pipelines.get(cfg.source_id).content.data
            )
            ds = DataSourceDataset(value_source, label_source)

            # TODO: more loader settings
            loader = DataLoader(ds, batch_size=cfg.batch_size, shuffle=cfg.shuffle_data)

            # Setup training
            optimizer = Adam(model.parameters(), lr=cfg.learning_rate)
            criterion = NLLLoss()

            process = mp.Process(target=train_model, args=(model, optimizer, criterion, loader, cfg.epochs, msg_queue))
            process.start()

            received_last_msg = False
            while received_last_msg:
                try:
                    model = msg_queue.get(False)
                    received_last_msg = True
                except:
                    await asyncio.sleep(0.1)

            process.join()

            # Save the updated model
            self.models.data_files.save_to(cfg.model_id, model.state_dict())

    def create_model(self, architecture: ArchitectureConfig, meta_data: MetaData) -> FileId:
        model = ArchitectureModel.create_from_architecture(architecture, self.layer_service)
        model_id = self.models.create(
            ModelObject(meta_data, model.state_dict(), architecture)
        )  # save the model to the file system

        return model_id

    async def add_to_training_queue(self, cfg: TrainingConfig):
        await self.training_queue.put(cfg)


def train_model(
    model: nn.Module,
    optimizer: optim.Optimizer,
    criterion: nn.Module,
    loader: DataLoader[tuple[Tensor, Tensor]],
    epochs: int,
    msg_queue: mp.Queue,
) -> None:
    # Training loop
    model.train()

    for epoch in range(epochs):
        for i, (x, y) in loader:

            # Forward pass
            outputs = model(x)
            loss = criterion(outputs, y)

            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        msg_queue.put(model)

    msg_queue.put(model)
