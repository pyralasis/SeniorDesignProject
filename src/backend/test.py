from pathlib import Path
from server.architecture.desc import (
    ArchitectureDescription,
    InputLayerDescription,
    NetworkLayerDescription,
)
from server.architecture.service import ArchitectureService
from server.layer.param import (
    BoolParameter,
    BoolParameterValue,
    IntParameterValue,
    ParameterValue,
)
from server.layer.size import TensorSize


arch = ArchitectureService(Path("./architectures"))
arch.load_all_architectures()


a = ArchitectureDescription(
    "Test",
    [InputLayerDescription(0, TensorSize((5, 32, 32)))],
    [
        NetworkLayerDescription(
            1,
            "linear",
            0,
            {"out_features": IntParameterValue(1), "bias": BoolParameterValue(True)},
        )
    ],
)

arch.save_architecture("test", a)
