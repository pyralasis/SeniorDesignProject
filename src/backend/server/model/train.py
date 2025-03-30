import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING

import torch.multiprocessing as mp
from server.data.sources.base import DataSourceDataset
from server.model.loss.config import LossConfig
from server.model.model import ArchitectureModel
from server.model.optim.config import OptimizerConfig
from server.util.file.file import FileId
from server.util.params import get_params_dict
from torch import Tensor, nn, optim
from torch.utils.data import DataLoader

if TYPE_CHECKING:
    from server.model.service import ModelService


@dataclass
class TrainingConfig:
    model_id: FileId
    source_id: FileId
    loss_fn: LossConfig
    optimizer: OptimizerConfig
    shuffle_data: bool = True
    batch_size: int = 32
    epochs: int = 10


async def training_thread(model_service: "ModelService"):
    while True:
        try:
            cfg = await model_service.training_queue.get()
            msg_queue = mp.Queue()

            # Load the model
            model_obj = model_service.models.get(cfg.model_id)
            model = ArchitectureModel.create_from_architecture(
                model_obj.content.architecture,
                model_service.layer_service,
            )
            model.load_state_dict(model_obj.content.data)

            # Load the data
            value_source, label_source = model_service.data_service.config_to_sources(
                model_service.data_service.pipelines.get(cfg.source_id).content.data
            )
            ds = DataSourceDataset(value_source, label_source)

            # TODO: more loader settings
            loader = DataLoader(ds, batch_size=cfg.batch_size, shuffle=cfg.shuffle_data)

            optimizer = model_service.optimizers.get(cfg.optimizer.id).constructor(
                model, **get_params_dict(cfg.optimizer.param_values)
            )

            criterion = model_service.loss_fns.get(cfg.loss_fn.id).constructor(
                **get_params_dict(cfg.loss_fn.param_values)
            )

            process = mp.Process(target=train_model, args=(model, optimizer, criterion, loader, cfg.epochs, msg_queue))
            process.start()

            print("starting process", process)

            received_last_msg = False
            while received_last_msg:
                try:
                    model = msg_queue.get(False)
                    print("received result")
                    received_last_msg = True
                except:
                    await asyncio.sleep(0.1)

            process.join()

            if isinstance(model, Exception):
                print("received err", model)
                continue

            # Save the updated model
            model_service.models.data_files.save_to(cfg.model_id, model.state_dict())
        except:
            import traceback

            traceback.print_exc()


def train_model(
    model: nn.Module,
    optimizer: optim.Optimizer,
    criterion: nn.Module,
    loader: DataLoader[tuple[Tensor, Tensor]],
    epochs: int,
    msg_queue: mp.Queue,
) -> None:
    print("started training")
    try:
        # Training loop
        model.train()

        for epoch in range(epochs):
            print("Epoch", epoch)
            for i, (x, y) in loader:

                # Forward pass
                outputs = model(x)
                loss = criterion(outputs, y)

                # Backward pass and optimize
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        msg_queue.put(model)
    except Exception as e:
        msg_queue.put(e)
