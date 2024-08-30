import importlib
import json

from .Exceptions import NonBytesInput


class File:

    @staticmethod
    def __raise(exception):
        raise exception

    @classmethod
    def pack(cls, name, data):
        if '.' not in name:
            return data if type(data) is bytes else cls.__raise(NonBytesInput(name))
        match name.split('.')[-1]:
            case 'json':
                return json.dumps(json.loads(data)) if type(data) is bytes else json.dumps(data)
            case 'txt':
                return data.decode() if type(data) is bytes \
                    else data if type(data) is str \
                    else cls.__raise(NonBytesInput(name))
            case 'zip':
                return data if type(data) is bytes else data.get_bytes()
            case _:
                return data if type(data) is bytes else cls.__raise(NonBytesInput(name))

    @staticmethod
    def unpack(name, data):
        if '.' not in name:
            return data
        match name.split('.')[-1]:
            case 'json':
                return json.loads(data)
            case 'txt':
                return data.decode() if type(data) is bytes else data
            case 'zip':
                return importlib.import_module(".main", 'zipmanager').ZipFolder(data)
            case _:
                return data
