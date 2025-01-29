from typing import TypeAlias

FileId: TypeAlias = int


def is_file_id(val: str) -> bool:
    return val.isdigit()
