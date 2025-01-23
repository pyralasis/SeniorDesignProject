from dataclasses import dataclass
from pathlib import Path

import pydantic
from server.architecture.config import (
    ArchitectureConfig,
    InputLayerConfig,
    NetworkLayerConfig,
)
from server.architecture.service import ArchitectureService
from server.params import (
    BoolParameter,
    BoolParameterValue,
    IntParameterValue,
    ParameterValue,
)
from server.layer.size import TensorSize


@dataclass
class NodeConfig:
    x: float
    y: float
    metadata: dict


adapter = pydantic.TypeAdapter(NodeConfig)

print(
    adapter.validate_json(
        """{
    "x": 1,
    "y": 1,
    "metadata": {
        "color": "#ffffff",
        "num": {
            "r": 1.0
        }
    }
}"""
    )
)
