from dataclasses import dataclass

from server.model.loss.definition import LossID
from server.params import AnyParameterValue


@dataclass
class LossConfig:
    id: LossID
    param_values: list[tuple[str, AnyParameterValue]]
