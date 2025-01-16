from pathlib import Path
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


# arch = ArchitectureService(Path("./architectures"))
# arch.load_all_architectures()


# a = ArchitectureDescription(
#     "Test",
#     [InputLayerDescription(0, TensorSize((5, 32, 32)))],
#     [
#         NetworkLayerDescription(
#             1,
#             "linear",
#             0,
#             {"out_features": IntParameterValue(1), "bias": BoolParameterValue(True)},
#         )
#     ],
# )

# arch.save_architecture("test", a)


def test(a, b, c, **_):
    print(a, b, c)


my_dict = {"a": 1, "b": 2, "c": 3, "d": 4}
test(**my_dict)
