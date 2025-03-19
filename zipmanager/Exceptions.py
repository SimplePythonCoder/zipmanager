
class NonBytesInput(Exception):
    def __init__(self, file_name):
        super().__init__(f'File "{file_name}" data must be bytes')


class BytesDecodeError(Exception):
    def __init__(self, file_name):
        super().__init__(f'File "{file_name}" data could not be decoded into the given extension')


class ZipDecodeError(Exception):
    def __init__(self, name=None):
        super().__init__('could not decode the given bytes into a zip format' if not name
                         else f'could not decode file "{name}" into a zip format')


class FileNameConflict(Exception):
    def __init__(self, file_name):
        super().__init__(f'File "{file_name}" already exists in the zip folder')


class FileNotFound(Exception):
    def __init__(self, file_name):
        super().__init__(f'File "{file_name}" does not exist in the zip folder')


class ExternalClassOperation(Exception):
    def __init__(self, type_name):
        super().__init__(f'type "{type_name.__name__}" cannot interact with the ZipFolder class')


class UnsupportedDataType(Exception):
    def __init__(self, type_name):
        super().__init__(f'the data type "{type_name.__name__}" cannot be converted into a ZipFolder object')


class Base64DecodingError(Exception):
    def __init__(self):
        super().__init__('could not decode the given base64 string')


class EmptyFileName(Exception):
    def __init__(self):
        super().__init__('cannot enter empty file name')


class PathNotFound(Exception):
    def __init__(self, path):
        super().__init__(f'cannot find the path "{path}"')


class UnsupportedOption(Exception):
    def __init__(self, option):
        super().__init__(f"option '{option}' is not supported")


class FormatError(Exception):
    def __init__(self, format_):
        if ' ' in format_:
            super().__init__(f"Space not allowed in string format")
        else:
            super().__init__(f"Invalid format string '{format_}'")

class UnknownRowOrColumn(Exception):
    def __init__(self):
        super().__init__('Invalid column or row')