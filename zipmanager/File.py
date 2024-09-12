import importlib
import json
import os
import pathlib
import re

from .Exceptions import NonBytesInput, PathNotFound, ZipDecodeError


class File:
    zipmanager = importlib.import_module(".main", 'zipmanager')

    @staticmethod
    def __raise(exc, *args, **kwargs):
        raise exc(*args, **kwargs) from None

    @classmethod
    def pack(cls, name, data):
        if cls.is_path(data):
            data = cls.open_file(data)
        if '.' not in name:
            return data if type(data) is bytes else cls.__raise(NonBytesInput, name)
        match name.split('.')[-1]:
            case 'json':
                return json.dumps(json.loads(data)) if type(data) is bytes else json.dumps(data)
            case 'txt' | 'py':
                return data.decode() if type(data) is bytes \
                    else data if type(data) is str \
                    else cls.__raise(NonBytesInput, name)
            case 'zip':
                return data if type(data) is bytes and cls.zipmanager.ZipFolder(data) \
                    else data.get_bytes() if data.__class__.__name__ == 'ZipFolder' \
                    else cls.__raise(ZipDecodeError, name)
            case _:
                return data if type(data) is bytes else cls.__raise(NonBytesInput, name)

    @classmethod
    def unpack(cls, name, data):
        if '.' not in name:
            return data
        match name.split('.')[-1]:
            case 'json':
                return json.loads(data)
            case 'txt' | 'py':
                return data.decode() if type(data) is bytes else data
            case 'zip':
                return cls.zipmanager.ZipFolder(data)
            case _:
                return data

    @classmethod
    def open_file(cls, file_path):
        if not os.path.exists(file_path):
            cls.__raise(PathNotFound, file_path)
        with open(file_path, 'rb') as fh:
            return fh.read()

    @classmethod
    def is_path(cls, txt: str):
        return type(txt) is str and (
                pathlib.Path(txt).is_file()
                or
                re.search(r'^(C:|\./|/)(/?[a-zA-Z0-9]+)+(\.[a-zA-Z0-9]*)$', txt)
        )
