import random
from pathlib import Path
from typing import Generic, TypeVar, TypeVarTuple

from .file import FileId
from .manager import (
    FileIdNotFoundError,
    IFileManager,
    INetworkFileManager,
    JsonFileManager,
)
from .meta import create_meta_file_manager
from .object import LoadableObjectProtocol, LoadedObject, ObjectDescription, ObjectInfo

TData = TypeVar("TData")
Ts = TypeVarTuple("Ts")
TObj = TypeVar("TObj", bound=LoadableObjectProtocol)


class IncorrectFileArgumentsError(Exception):
    def __init__(self, recv_arg_count: int, req_arg_count: int):
        super().__init__(f"Expected data for {req_arg_count} files but received data for {recv_arg_count} files. ")
        self.recv_arg_count = recv_arg_count
        self.req_arg_count = req_arg_count


class FileCoordinator(Generic[TObj, TData, *Ts]):
    def __init__(
        self,
        obj_type: type[TObj],
        api_name: str,
        data_file_manager: IFileManager[TData],
        extra_files: list[INetworkFileManager],
        save_path: Path,
    ) -> None:
        self.obj_type = obj_type
        self.api_name = api_name
        self.info_files = JsonFileManager("info", save_path, ObjectInfo, ".info.json")
        self.meta_files = create_meta_file_manager(save_path)
        self.data_files = data_file_manager
        self.extra_files = extra_files

    def create(self, obj: TObj) -> FileId:
        id = self._generate_id()

        self._save_files(id, obj)
        self.info_files.save_to(id, ObjectInfo(0))

        return id

    def update(self, id: FileId, obj: TObj):
        if self.exists(id):
            self._save_files(id, obj)
            self.increment_version(id)
        else:
            raise FileIdNotFoundError(id)

    def delete(self, id: FileId):
        if self.exists(id):
            self.info_files.delete(id)
            self.meta_files.delete(id)
            self.data_files.delete(id)

            for file_manager in self.extra_files:
                file_manager.delete(id)
        else:
            raise FileIdNotFoundError(id)

    def _save_files(self, id: FileId, obj: TObj):
        data = obj.data
        meta_data = obj.meta
        extra = obj.extra()

        if len(extra) != len(self.extra_files):
            raise IncorrectFileArgumentsError(len(extra), len(self.extra_files))

        self.data_files.save_to(id, data)
        self.meta_files.save_to(id, meta_data)

        for i in range(len(self.extra_files)):
            self.extra_files[i].save_to(id, extra[i])

    def increment_version(self, id: FileId):
        file_info = self.info_files.load(id)
        file_info.version += 1
        self.info_files.save_to(id, file_info)

    def get(self, id: FileId) -> LoadedObject[TObj]:
        extra_data = []
        for file_manager in self.extra_files:
            extra_data.append(file_manager.load(id))

        return LoadedObject(
            id, self.info_files.load(id), self.obj_type(self.meta_files.load(id), self.data_files.load(id), *extra_data)
        )

    def get_all(self) -> list[LoadedObject[TObj]]:
        return [self.get(id) for id in self.meta_files.available()]

    def available(self) -> list[ObjectDescription]:
        return [
            ObjectDescription(id, self.info_files.load(id), self.meta_files.load(id))
            for id in self.info_files.available()
        ]

    def available_ids(self) -> list[FileId]:
        # TODO: Check to make sure all files exist?
        return self.info_files.available()

    def exists(self, id: FileId):
        return self.info_files.exists(id)

    def _generate_id(self) -> FileId:
        id = random.randint(1, 1000000000)

        while self.exists(id):
            id = random.randint(1, 1000000000)

        return id
