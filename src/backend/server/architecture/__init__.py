__all__ = ["ArchitectureConfig", "InputLayerConfig", "NetworkLayerConfig", "ArchitectureService"]

"""
This is a module containing the data structures and logic for managing 
Architectures. Architectures are 'blueprints' for pytorch models. They
include all layers in a model and the parameter values.
"""

from .config import ArchitectureConfig, InputLayerConfig, NetworkLayerConfig
from .service import ArchitectureService
