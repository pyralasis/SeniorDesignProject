from typing import TypeVar

T = TypeVar("T")

def override(fn: T) -> T:
    return fn