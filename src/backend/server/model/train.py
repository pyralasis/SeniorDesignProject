import asyncio
from dataclasses import dataclass
from queue import Empty
from typing import TYPE_CHECKING, Any, Literal, TypeAlias

import torch
import torch.multiprocessing as mp
from server.data.sources.base import DataSourceDataset
from server.model.loss.config import LossConfig
from server.model.model import ArchitectureModel
from server.model.optim.config import OptimizerConfig
from server.util.file.file import FileId
from server.util.file.meta import MetaData
from server.util.file.object import Loadable
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
    device: str = "cpu"
    shuffle_data: bool = True
    batch_size: int = 32
    epochs: int = 10


@dataclass
class TrainingQueuedInfo:
    status: Literal["queued"] = "queued"


@dataclass
class TrainingInProgressInfo:
    epoch: int
    avg_loss: float
    status: Literal["in_progress"] = "in_progress"


@dataclass
class TrainingCompleteInfo:
    avg_loss: float
    status: Literal["complete"] = "complete"


@dataclass
class TrainingFailedInfo:
    reason: str
    description: str
    status: Literal["failed"] = "failed"


TrainingInfo: TypeAlias = TrainingQueuedInfo | TrainingInProgressInfo | TrainingCompleteInfo | TrainingFailedInfo


@dataclass
class TrainLogObject(Loadable):
    meta: MetaData
    data: TrainingInfo
    config: TrainingConfig


async def training_thread(model_service: "ModelService"):
    while True:
        try:
            process = None

            log_file, cfg = await model_service.training_queue.get()

            try:
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
                loader = DataLoader(ds, batch_size=cfg.batch_size, shuffle=cfg.shuffle_data, num_workers=0)

                optimizer = model_service.optimizers.get(cfg.optimizer.id).constructor(
                    model, **get_params_dict(cfg.optimizer.param_values)
                )

                criterion = model_service.loss_fns.get(cfg.loss_fn.id).constructor(
                    **get_params_dict(cfg.loss_fn.param_values)
                )

                process = mp.Process(
                    target=train_model, args=(model, optimizer, criterion, loader, cfg.epochs, cfg.device, msg_queue)
                )
                process.start()

                model_service.train_logs.data_files.save_to(log_file, TrainingInProgressInfo(0, 10000))
                model_service.train_logs.increment_version(log_file)

                received_last_msg = False
                while not received_last_msg:
                    try:
                        msg = msg_queue.get(False)
                        match msg.type:
                            case "epoch_complete":
                                model_service.train_logs.data_files.save_to(
                                    log_file, TrainingInProgressInfo(msg.epoch, msg.avg_loss)
                                )
                                model_service.train_logs.increment_version(log_file)

                            case "failure":
                                model_service.train_logs.data_files.save_to(
                                    log_file, TrainingFailedInfo("error", msg.description)
                                )
                                model_service.train_logs.increment_version(log_file)
                                received_last_msg = True
                                process.kill()

                            case "finished":
                                model_service.train_logs.data_files.save_to(
                                    log_file, TrainingCompleteInfo(msg.avg_loss)
                                )
                                model_service.train_logs.increment_version(log_file)
                                model_service.models.data_files.save_to(cfg.model_id, msg.model.state_dict())
                                model_service.models.increment_version(cfg.model_id)
                                received_last_msg = True
                                process.join()
                    except Empty:
                        await asyncio.sleep(0.1)

            except (KeyboardInterrupt, asyncio.CancelledError) as e:
                if process is not None:
                    process.kill()
                model_service.train_logs.data_files.save_to(
                    log_file, TrainingFailedInfo("interrupted", "Training was interrupted in progress")
                )
                model_service.train_logs.increment_version(log_file)
                raise e
            except Exception as e:
                if process is not None:
                    process.kill()
                model_service.train_logs.data_files.save_to(log_file, TrainingFailedInfo("error", str(e)))
                model_service.train_logs.increment_version(log_file)
                received_last_msg = True

        except (KeyboardInterrupt, asyncio.CancelledError) as e:
            while not model_service.training_queue.empty():
                log_file, cfg = model_service.training_queue.get_nowait()
                model_service.train_logs.data_files.save_to(
                    log_file, TrainingFailedInfo("interrupted", "Training was interrupted while queued")
                )
                model_service.train_logs.increment_version(log_file)

            raise e
        except:
            import traceback

            traceback.print_exc()


@dataclass
class TrainingFinishedMsg(Loadable):
    avg_loss: float
    model: nn.Module
    type: Literal["finished"] = "finished"


@dataclass
class EpochCompleteMsg(Loadable):
    epoch: int
    avg_loss: float
    type: Literal["epoch_complete"] = "epoch_complete"


@dataclass
class TrainingFailureMsg(Loadable):
    reason: str
    description: str
    type: Literal["failure"] = "failure"


TrainingMsg = TrainingFinishedMsg | EpochCompleteMsg | TrainingFailureMsg


def train_model(
    model: nn.Module,
    optimizer: optim.Optimizer,
    criterion: nn.Module,
    loader: DataLoader[tuple[Tensor, Tensor]],
    epochs: int,
    device: str,
    msg_queue: "mp.Queue[TrainingMsg]",
) -> None:
    try:
        torch_device = torch.device(device)

        # Training loop
        model = model.to(torch_device)
        model.train()

        for epoch in range(epochs):

            total_loss = 0
            for i, (x, y) in enumerate(loader):
                x = x.to(torch_device)
                y = y.to(torch_device)

                # Forward pass
                outputs = model([x])
                loss = criterion(outputs, y)

                # Backward pass and optimize
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_loss += torch.sum(loss).item()

            avg_loss = total_loss / len(loader)
            msg_queue.put(EpochCompleteMsg(epoch + 1, avg_loss))

        msg_queue.put(TrainingFinishedMsg(avg_loss, model))
    except Exception as e:
        msg_queue.put(TrainingFailureMsg("error", str(e)))
        import traceback

        traceback.print_exc()
