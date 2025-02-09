from dataclasses import dataclass
from pathlib import Path

from server.architecture.config import LayerInstanceID
from server.util.file import JsonFileManager


@dataclass
class NodeConfig:
    x: float
    y: float
    metadata: dict


@dataclass
class LayoutConfig:
    """
    Configuration class for defining the layout of a node.
    """

    nodes: dict[LayerInstanceID, NodeConfig]
    edges: list[dict]


def create_layout_file_manager(save_path: Path):
    return JsonFileManager("layout", save_path, LayoutConfig, ".layout.json")
