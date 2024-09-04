import binascii
import io
import zipfile
import base64
from json.decoder import JSONDecodeError

from .Exceptions import (FileNameConflict, ExternalClassOperation,
                         FileNotFound, BytesDecodeError, UnsupportedDataType,
                         Base64DecodingError, EmptyFileName)
from .File import File


class ZipFolder:

    def __init__(self, data):
        """
        the data for the zip can be one of the following:

        - dictionary of file names as keys and file data as value (file data can be bytes, str for .txt or dict/list for .json).
        - base64 str of a zip (from the get_b64 function)
        - zip bytes (from the get_bytes function)

        :param data:                the data for the zip
        :type data:                 dict[str, dict] | dict[str, str] | dict[str, bytes] | str | bytes
        """
        match data:
            case dict():
                self.__raw_zip = self.__create_zip(data)
            case str():
                self.__raw_zip = self.__b64_to_zip(data)
            case bytes():
                self.__raw_zip = self.__bytes_to_zip(data)
            case _:
                raise UnsupportedDataType(type(data))

    def __eq__(self, other):
        self.__check_class(other)
        return self.get_bytes() == other.get_bytes()

    def __add__(self, other):
        self.__check_class(other)
        self.add_files(other.raw_files())
        return self

    def __getitem__(self, file_name: str):
        if file_name in self.file_list:
            return File.unpack(file_name, self.__raw_zip.open(file_name).read())
        raise FileNotFound(file_name)

    def __str__(self):
        return (f'Zipfile Object {hex(id(self)).upper()} / '
                f'file number: {len(self.file_list)} / '
                f'size: {self.get_size():,} bytes / '
                f'compressed size: {self.get_size(compressed=True):,} bytes')

    def get_size(self, file_name=None, compressed=False):
        """
        returns the size of a file or the entire zip.
        can return both compressed and normal size.

        :param file_name:           this will return the size of a specific file (disabled by default)
        :type file_name:            str
        :param compressed:          if true will return the compressed size (false by default)
        :type compressed:           bool
        :return:                    size in bytes of a file or the entire zip
        :rtype:                     int
        """
        size = 0
        match file_name:
            case str():
                if file_name in self.file_list:
                    return getattr(self.__raw_zip.getinfo(file_name), 'compress_size' if compressed else 'file_size')
                raise FileNotFound(file_name)
            case _:
                for file in self.__raw_zip.filelist:
                    size += getattr(file, 'compress_size' if compressed else 'file_size')
        return size

    def get(self, file_name):
        """
        used to get the data of a specific file.
        if file not in zip, this will return null instead.

        :param file_name:       file name (if inside a folder add 'folder_name/' before the file name)
        :type file_name:        str
        :return:
        """
        if file_name in self.file_list:
            return File.unpack(file_name, self.__raw_zip.open(file_name).read())
        return None

    def add_files(self, data):
        """
        add files to the zip file.
        you can add folders by adding the folder name before the filename separated by a '/'.

        :param data:            dict of filename as key and data as value
        :type data:             dict[str, dict] | dict[str, str] | dict[str, bytes]
        """
        for file in data.keys():
            if file in self.file_list:
                raise FileNameConflict(file)
        self.__raw_zip = self.__create_zip(dict(self.raw_files(), **data))

    def delete_file(self, file_name):
        """
        deletes files from the zip file.

        :param file_name:            file name (if inside a folder add 'folder_name/' before the file name)
        :type file_name:             str
        :return:                    success status of the deletion (file not found will return False)
        :rtype:                     bool
        """
        if file_name in self.file_list:
            self.__raw_zip = self.__edit_zip([file for file in self.file_list if file != file_name])
            return True
        return False

    def raw_files(self):
        """
        used to get a dictionary of all files with file names as keys and data as value.
        :return:    A dict of all files as name, data pairs.
        :rtype:      dict
        """
        return {file: File.unpack(file, self.__raw_zip.open(file).read())
                for file in self.file_list}

    @property
    def file_list(self):
        return [file.filename for file in self.__raw_zip.filelist]

    def get_b64(self):
        """
        the string this function returns can be used in several ways:

        - saving multiple zip into a single file
        - sending text with an api instead of bytes
        - ZipFolder can read it and convert it to a zip

        :return:        a base64 string of the zip bytes
        :rtype:         str
        """
        return base64.b64encode(self.get_bytes()).decode()

    def get_bytes(self):
        """
        used to get the raw bytes of the zip.
        ZipFolder can use this response to create an identical zip - ZipFolder(some_zipfolder.get_bytes()).

        :return:        the bytes of the zip
        :rtype:         bytes
        """
        return self.__edit_zip(byte=True).read()

    def __check_class(self, other):
        if type(self) is not type(other):
            raise ExternalClassOperation(type(other))

    @staticmethod
    def __create_zip(files):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as file_zip:
            for file_name, data in files.items():
                if not file_name:
                    raise EmptyFileName
                try:
                    file_zip.writestr(f'{file_name}', data=File.pack(file_name, data))
                except (UnicodeDecodeError, JSONDecodeError):
                    raise BytesDecodeError(file_name)

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
        try:
            return zipfile.ZipFile(io.BytesIO(base64.b64decode(data)), 'r')
        except binascii.Error:
            raise Base64DecodingError

    def save(self, path_with_name='./temp.zip'):
        """
        saves the zip folder to the given location.
        path must be with name (extension optional).
        :param path_with_name:      path for save location (empty will save it to current folder)
        :type path_with_name:       str
        :return:
        """
        with open(path_with_name if path_with_name.endswith('.zip') else path_with_name + '.zip', 'wb') as zfh:
            zfh.write(self.get_bytes())
