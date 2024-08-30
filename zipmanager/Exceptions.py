
class NonBytesInput(Exception):
    def __init__(self, file_name):
        super().__init__(f'File {file_name} data must be bytes')


class BytesDecodeError(Exception):
    def __init__(self, file_name):
        super().__init__(f'File {file_name} data could not be decoded into the given extension')


class FileNameConflict(Exception):
    def __init__(self, file_name):
        super().__init__(f'File {file_name} already exists in the zip folder')


class FileNotFound(Exception):
    def __init__(self, file_name):
        super().__init__(f'File {file_name} does no exist in the zip folder')


class ExternalClassOperation(Exception):
    def __init__(self, type_name):
        super().__init__(f'type {type_name.__name__} cannot interact with the ZipFile class')
