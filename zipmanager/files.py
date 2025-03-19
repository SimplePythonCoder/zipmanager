import os
import re
from .Exceptions import UnknownRowOrColumn

class BaseFile:
    def __init__(self, encoded):
        self.encoded = encoded

    def __str__(self):
        return self.encoded.decode()

    @staticmethod
    def _raise(exc, *args, **kwargs):
        raise exc(*args, **kwargs) from None

class Markdown(BaseFile):

    def __main_md(self, print_=False):
        new_data = []
        is_code = False
        under_line = '\u001b[4m'
        end = '\u001b[0m'
        for line in str(self).split('\n'):
            line = str(line)
            if line.startswith("```"):
                is_code = not is_code
            if not is_code:
                if re.search('#+ ', line):
                    new_data.append(f'{under_line}{re.sub(r"#+ ", "", line)}{end}') if print_ \
                    else new_data.append(re.sub(r"#+ ", "", line))
                    continue
                elif re.search('-', line):
                    new_data.append(f'{re.sub(r"- ", "• ", line)}')
                    continue
            new_data.append(line)
        return '\n'.join(new_data)

    def md(self):
        """
        returning a markdown file using markdown features

        :return:    string of markdown file
        :rtype:     str
        """
        return self.__main_md()

    def print_md(self):
        """
        printing a markdown file using markdown features

        :rtype: None
        """
        os.system('') # necessary for ANSI terminal printing
        print(self.__main_md(print_=True))


class CSV(BaseFile):
    def __init__(self, encoded):
        super().__init__(encoded)
        self.__table = str(self).split('\n')
        self.__headers = list(self.__table.pop(0).split(','))

    def __full_csv(self):
        final_dict = {}
        for index, line in enumerate(self.__table):
            final_dict[index+1] = dict(zip(self.__headers, line.split(',')))
        return final_dict

    def csv(self, row=None, col=None):
        if row is None and col is None:
            return self.__full_csv()
        match [bool(type(row) is int and row > 0), type(col) is str and col in self.__headers]:
            case [True, True]:
                return self.__table[row-1].split(',')[self.__headers.index(col)]
            case [True, False]:
                return self.__table[row-1].split(',')
            case [False, True]:
                return {index+1: line.split(',')[self.__headers.index(col)] for index, line in enumerate(self.__table)}
            case [False, False]:
                self._raise(UnknownRowOrColumn)
