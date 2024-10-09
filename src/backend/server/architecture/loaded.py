from dataclasses import dataclass
from pathlib import Path

from server.architecture.desc import ArchitectureDescription


@dataclass
class LoadedArchitecture:
    file_name: str
    description: ArchitectureDescription