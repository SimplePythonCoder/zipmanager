import io
import zipfile
import base64

from .Exceptions import FileNameConflict, ExternalClassOperation, FileNotFound
from .File import File


class ZipFolder:

    def __init__(self, data: dict[str, dict] | dict[str, str] | dict[str, bytes] | str | bytes):
        match data:
            case dict():
                self.__raw_zip = self.__create_zip(data)
            case str():
                self.__raw_zip = self.__b64_to_zip(data)
            case bytes():
                self.__raw_zip = self.__bytes_to_zip(data)

    def __eq__(self, other):
        self.__check_class(other)
        return self.raw_files() == other.raw_files()

    def __add__(self, other):
        self.__check_class(other)
        self.add_files(other.raw_files())
        return self

    def __getitem__(self, file_name):
        if file_name in self.file_list:
            return File.unpack(file_name, self.__raw_zip.open(file_name).read())
        raise FileNotFound(file_name)

    def __str__(self):
        return (f'Zipfile Object {hex(id(self)).upper()} / '
                f'file number: {len(self.file_list)} / '
                f'size: {self.get_size():,} bytes / '
                f'compressed size: {self.get_size(compressed=True):,} bytes')

    def get_size(self, file_name=None, compressed=False):
        size = 0
        match file_name:
            case str():
                if file_name in self.file_list:
                    return getattr(self.__raw_zip.getinfo(file_name), 'compress_size' if compressed else 'file_size')
                else:
                    raise FileNotFound(file_name)
            case _:
                for file in self.__raw_zip.filelist:
                    size += getattr(file, 'compress_size' if compressed else 'file_size')
        return size

    def get(self, file_name):
        if file_name in self.file_list:
            return File.unpack(file_name, self.__raw_zip.open(file_name).read())
        return None

    def add_files(self, data):
        """
        add files to the zip file.
        you can add folders by adding the folder name before the filename separated by a '/'.
        :param data:            dict of filename as key and data as value
        :type data:             dict[str, dict] | dict[str, str] | dict[str, bytes]
        :return:
        """
        for file in data.keys():
            if file in self.file_list:
                raise FileNameConflict(file)
        self.__raw_zip = self.__create_zip(dict(self.raw_files(), **data))

    def delete_file(self, file_name):
        if file_name in self.file_list:
            self.__raw_zip = self.__edit_zip([file for file in self.file_list if file != file_name])

    def raw_files(self):
        return {file: File.unpack(file, self.__raw_zip.open(file).read())
                for file in self.file_list}

    @property
    def file_list(self):
        return [file.filename for file in self.__raw_zip.filelist]

    def get_b64(self):
        return base64.b64encode(self.__edit_zip(byte=True).read()).decode()

    def __check_class(self, other):
        if type(self) is not type(other):
            raise ExternalClassOperation(type(other))

    @staticmethod
    def __create_zip(files):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as file_zip:
            for file_name, data in files.items():
                file_zip.writestr(f'{file_name}', data=File.pack(file_name, data))
        zip_buffer.seek(0)
        return zipfile.ZipFile(zip_buffer, 'r')

    def __edit_zip(self, files=None, byte=False):
        if files is None:
            files = self.file_list
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as file_zip:
            for file_name in files:
                file_zip.writestr(f'{file_name}', data=File.pack(file_name, self[file_name]))
        zip_buffer.seek(0)
        return zipfile.ZipFile(zip_buffer, 'r') if not byte else zip_buffer

    @staticmethod
    def __bytes_to_zip(data):
        return zipfile.ZipFile(io.BytesIO(data), 'r')

    @staticmethod
    def __b64_to_zip(data):
        return zipfile.ZipFile(io.BytesIO(base64.b64decode(data)), 'r')

    def save(self, path_with_name='./temp.zip'):
        """
        saves the zip folder to the given location.
        path must be with name (extension optional).
        :param path_with_name:      path for save location (empty will save it to current folder)
        :type path_with_name:       str
        :return:
        """
        with open(path_with_name if path_with_name.endswith('.zip') else path_with_name + '.zip', 'wb') as zfh:
            zfh.write(self.__edit_zip(byte=True).read())
