import asyncio
import time
from dataclasses import dataclass
from queue import Empty
from typing import TYPE_CHECKING, Any, Literal, OrderedDict, TypeAlias

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

    shuffle_data: bool = True
    batch_size: int = 32
    epochs: int = 10

    device: str = "cpu"
    loader_workers: int = 0
    pin_memory: bool = False
    prefetch_factor: int = 2
    persistent_workers: bool = False


@dataclass
class TrainingQueuedInfo:
    queue_time: int
    status: Literal["queued"] = "queued"


@dataclass
class TrainingInProgressInfo:
    start_time: int
    avg_time_per_epoch: int
    epoch: int
    avg_loss: float
    status: Literal["in_progress"] = "in_progress"


@dataclass
class TrainingCompleteInfo:
    start_time: int
    end_time: int
    avg_time_per_epoch: int
    avg_loss: float
    status: Literal["complete"] = "complete"


@dataclass
class TrainingFailedInfo:
    start_time: int
    end_time: int
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
    start_time = None
    while True:
        try:
            process = None

            log_file, cfg = await model_service.training_queue.get()

            try:
                msg_queue = mp.Queue()

                # Load the model
                model = model_service.load_model(cfg.model_id)

                # Load the data
                value_source, label_source = model_service.data_service.config_to_sources(
                    model_service.data_service.pipelines.get(cfg.source_id).content.data
                )
                ds = DataSourceDataset(value_source, label_source)

                # TODO: more loader settings
                loader = DataLoader(
                    ds,
                    batch_size=cfg.batch_size,
                    shuffle=cfg.shuffle_data,
                    num_workers=cfg.loader_workers,
                    pin_memory=cfg.pin_memory,
                    pin_memory_device=cfg.device if cfg.pin_memory else "",
                    prefetch_factor=cfg.prefetch_factor if cfg.loader_workers > 0 else None,
                    persistent_workers=cfg.persistent_workers,
                )

                optimizer = model_service.optimizers.get(cfg.optimizer.id).constructor(
                    model, **get_params_dict(cfg.optimizer.param_values)
                )

                criterion = model_service.loss_fns.get(cfg.loss_fn.id).constructor(
                    **get_params_dict(cfg.loss_fn.param_values)
                )

                # asyncio.to_thread()
                process = mp.Process(
                    target=train_model, args=(model, optimizer, criterion, loader, cfg.epochs, cfg.device, msg_queue)
                )

                await asyncio.to_thread(process.start)

                start_time = get_time()

                model_service.train_logs.data_files.save_to(log_file, TrainingInProgressInfo(start_time, 0, 0, 10000))
                model_service.train_logs.increment_version(log_file)

                received_last_msg = False
                while not received_last_msg:
                    try:
                        msg: TrainingMsg = msg_queue.get(False)
                        match msg.type:
                            case "epoch_complete":
                                cur_time = get_time()
                                avg_time_per_epoch = (cur_time - start_time) // msg.epoch

                                model_service.train_logs.data_files.save_to(
                                    log_file,
                                    TrainingInProgressInfo(start_time, avg_time_per_epoch, msg.epoch, msg.avg_loss),
                                )
                                model_service.train_logs.increment_version(log_file)

                            case "failure":
                                cur_time = get_time()
                                model_service.train_logs.data_files.save_to(
                                    log_file, TrainingFailedInfo(start_time, cur_time, "error", msg.description)
                                )
                                model_service.train_logs.increment_version(log_file)
                                received_last_msg = True
                                process.kill()

                            case "finished":
                                cur_time = get_time()
                                avg_time_per_epoch = (cur_time - start_time) // cfg.epochs

                                model_service.train_logs.data_files.save_to(
                                    log_file,
                                    TrainingCompleteInfo(start_time, cur_time, avg_time_per_epoch, msg.avg_loss),
                                )
                                model_service.train_logs.increment_version(log_file)
                                model_service.models.data_files.save_to(cfg.model_id, msg.model)
                                model_service.models.increment_version(cfg.model_id)
                                received_last_msg = True
                                process.join()
                    except Empty:
                        await asyncio.sleep(0.1)

            except (KeyboardInterrupt, asyncio.CancelledError) as e:
                if process is not None:
                    process.kill()

                cur_time = get_time()
                model_service.train_logs.data_files.save_to(
                    log_file,
                    TrainingFailedInfo(
                        start_time or 0, cur_time, "interrupted", "Training was interrupted in progress"
                    ),
                )
                model_service.train_logs.increment_version(log_file)
                raise e
            except Exception as e:
                if process is not None:
                    process.kill()
                cur_time = get_time()
                model_service.train_logs.data_files.save_to(
                    log_file, TrainingFailedInfo(start_time or 0, cur_time, "error", str(e))
                )
                model_service.train_logs.increment_version(log_file)
                received_last_msg = True

        except (KeyboardInterrupt, asyncio.CancelledError) as e:
            while not model_service.training_queue.empty():
                log_file, cfg = model_service.training_queue.get_nowait()
                model_service.train_logs.data_files.save_to(
                    log_file, TrainingFailedInfo(0, 0, "interrupted", "Training was interrupted while queued")
                )
                model_service.train_logs.increment_version(log_file)

            raise e
        except:
            import traceback

            traceback.print_exc()


@dataclass
class TrainingFinishedMsg(Loadable):
    avg_loss: float
    model: dict[str, Any]
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
        model=model.to(torch.device("cpu"))
        msg_queue.put(TrainingFinishedMsg(avg_loss, model.state_dict()))
    except Exception as e:
        msg_queue.put(TrainingFailureMsg("error", str(e)))
        import traceback

        traceback.print_exc()


def get_time() -> int:
    return int(time.time() * 1000)
