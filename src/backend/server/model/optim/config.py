from dataclasses import dataclass

from server.model.optim.definition import OptimID
from server.params import AnyParameterValue


@dataclass
class OptimizerConfig:
    id: OptimID
    param_values: list[tuple[str, AnyParameterValue]]
