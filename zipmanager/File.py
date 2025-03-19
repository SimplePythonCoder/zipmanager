import importlib
import json
import os
import pathlib
import re
from datetime import datetime

from .Exceptions import NonBytesInput, PathNotFound, ZipDecodeError
from .files import Markdown, CSV


class File:
    """
    used for file specific functions.
    """
    zipmanager = importlib.import_module(".main", 'zipmanager')

    @staticmethod
    def __raise(exc, *args, **kwargs):
        raise exc(*args, **kwargs) from None

    @classmethod
    def get_extension(cls, name):
        return name.split('.')[1] if '.' in name else ''

    @classmethod
    def create_base(cls, extension=None):
        """
        used to create base file for a given extension

        :param extension:       extension name
        :type extension:        str
        :return:                a base file to use for the given file type
        """
        match extension:
            case 'txt' | 'py' | 'md':
                return ''
            case 'json':
                return {}
            case 'list':
                return []
            case 'zip':
                return cls.zipmanager.ZipFolder({}).get_bytes()
            case 'html':
                return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    '
                        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n    '
                        '<title></title>\n</head>\n<body>\n\n</body>\n</html>')
            case 'java':
                return 'public static void main(String[] args){\n\n}'
            case _:
                return b''

    @classmethod
    def pack(cls, name, data):
        if cls.is_path(data):
            data = cls.open_file(data)
        if '.' not in name:
            return data if type(data) is bytes else cls.__raise(NonBytesInput, name)
        match name.split('.')[-1]:
            case 'json':
                return json.dumps(json.loads(data)) if type(data) is bytes else json.dumps(data)
            case 'txt' | 'py' | 'html' | 'java':
                return data.decode() if type(data) is bytes \
                    else data if type(data) is str \
                    else cls.__raise(NonBytesInput, name)
            case  'md':
                return data if type(data) in [str, bytes] \
                else data.encoded if data.__class__.__name__ == 'Markdown'\
                else cls.__raise(NonBytesInput, name)
            case  'csv':
                return data if type(data) in [str, bytes] \
                else data.encoded if data.__class__.__name__ == 'CSV'\
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
            case 'txt' | 'py' | 'html' | 'java':
                return data.decode() if type(data) is bytes else data
            case 'md':
                return Markdown(data)
            case 'csv':
                return CSV(data)
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


class MetaData:
    """
    A simple metadata object for extra data
    """
    def __init__(self, z_info):
        self.creation_datetime = datetime(*z_info.date_time)
        self.size = z_info.file_size
        self.compress_size = z_info.compress_size
        self.original_filename = z_info.filename


create_base = File.create_base
