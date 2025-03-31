from dataclasses import dataclass
from typing import Literal


@dataclass
class InvalidRequestErrResponse:
    msg: str
    success: Literal[False] = False
    error_type: Literal["invalid_request"] = "invalid_request"
