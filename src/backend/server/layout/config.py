from dataclasses import dataclass

from server.architecture.config import LayerInstanceID


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
