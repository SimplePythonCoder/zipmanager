import re
import csv
from io import StringIO

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
    def __init__(self, encoded):
        super().__init__(encoded)

    ANSI_RESET = "\033[0m"
    ANSI_BOLD = "\033[1m"
    ANSI_UNDERLINE = "\033[4m"
    ANSI_ITALIC = "\033[3m"
    ANSI_YELLOW = "\033[33m"
    ANSI_CYAN = "\033[36m"
    ANSI_MAGENTA = "\033[35m"
    ANSI_GREEN = "\033[32m"
    ANSI_BLUE = "\033[34m"

    def __main_md(self, print_=False):
        new_data = []
        is_code = False
        for line in str(self).split('\n'):
            line = str(line)
            if line.startswith("```"):
                is_code = not is_code
                line = f'{self.ANSI_BOLD}{self.ANSI_GREEN}{line}{self.ANSI_RESET}'
            if not is_code:
                if re.search(r'(?!:\\)#+ ', line) and not line.startswith('\\'):
                    line = (f'{self.ANSI_UNDERLINE}'
                            f'{self.ANSI_BOLD if line.startswith("# ") else ""}'
                            f'{self.ANSI_ITALIC if line.startswith("## ") else ""}'
                            f'{re.sub(r"#+ ", "", line)}{self.ANSI_RESET}')\
                    if print_ else new_data.append(re.sub(r"#+ ", "", line))
                if re.search(r'^(?!:\\)-', line):
                    line = f'{re.sub(r"- ", "• ", line)}'
                if re.search(r'\\.', line):
                    line = re.sub(r'\\', '', line)
                if re.search('`.+`', line):
                    line = re.sub('`([^`]+)`', fr'{self.ANSI_BOLD}{self.ANSI_GREEN}\1{self.ANSI_RESET}', line)
                if re.search('\*\*.+\*\*', line):
                    line = re.sub('\*\*([^*]+)\*\*', fr'{self.ANSI_BOLD}\1{self.ANSI_RESET}', line)

            else:
                line = f'{self.ANSI_GREEN}{line}{self.ANSI_RESET}'
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
        print(self.__main_md(print_=True))


class CSV(BaseFile):
    def __init__(self, encoded):
        super().__init__(encoded)
        self.__table = str(self).split('\n')
        self.__headers = list(self.__table.pop(0).split(','))
        self.__can_print = True
        for line in self.__table:
            if len(line) > len(self.__headers):
                self.__can_print = False

    def __full_csv(self):
        final_dict = {
            index: row for index, row in
            enumerate(csv.DictReader(StringIO(self.__str__())), start=1)
        }
        return final_dict

    def csv(self, row=None, col=None):
        """
        returns a csv with rows and columns as a dict.

        :param row:         (optional) row number in csv.
        :type row:          int
        :param col:         (optional) column in csv.
        :type col:          str
        :return:            dict of csv, row or column
        :rtype:             dict
        """
        if not self.__str__():
            return None
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
        return None

    def print_csv(self):
        if not self.__str__():
            return
        if not self.__can_print:
            self._raise(UnknownRowOrColumn) # extra column in row
        reader = csv.reader(StringIO(self.__str__()))
        rows = list(reader)
        headers = rows[0]
        column_widths = [len(header) for header in headers]
        for row in rows[1:]:
            for i, value in enumerate(row):
                column_widths[i] = max(column_widths[i], len(value))
        print(" | ".join(header.center(column_widths[i]) for i, header in enumerate(headers)))
        print("-" * (sum(column_widths) + ((len(column_widths) - 1) * 3)))
        for row in rows[1:]:
            print(" | ".join(value.ljust(column_widths[i]) for i, value in enumerate(row)))

