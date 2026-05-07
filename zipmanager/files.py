import re
import csv
from io import StringIO
import os

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

    ANSI_RED = "\033[31m"
    ANSI_YELLOW = "\033[33m"
    ANSI_CYAN = "\033[36m"
    ANSI_MAGENTA = "\033[35m"
    ANSI_GREEN = "\033[32m"
    ANSI_BLUE = "\033[34m"

    def _main_md(self, print_=False):
        new_data = []
        is_code = False
        for line in str(self).split('\n'):
            line = str(line)
            if line.startswith("```") and print_:
                is_code = not is_code
                line = f'{self.ANSI_BOLD}{self.ANSI_GREEN}{line}{self.ANSI_RESET}'
            if not is_code:
                if re.search(r'(?!:\\)#+ ', line) and not line.startswith('\\'):
                    line = (f'{self.ANSI_UNDERLINE}'
                            f'{self.ANSI_BOLD if line.startswith("# ") else ""}'
                            f'{self.ANSI_ITALIC if line.startswith("## ") else ""}'
                            f'{re.sub(r"#+ ", "", line)}{self.ANSI_RESET}')\
                    if print_ else re.sub(r"#+ ", "", line)
                if re.search(r'^(?!:\\)-', line):
                    line = f'{re.sub(r"- ", "• ", line)}'
                if re.search(r'\\.', str(line)):
                    line = re.sub(r'\\', '', line)
                if re.search('`.+`', str(line)) and print_:
                    line = re.sub('`([^`]+)`', fr'{self.ANSI_BOLD}{self.ANSI_GREEN}\1{self.ANSI_RESET}', line)
                if re.search('\*\*.+\*\*', str(line)) and print_:
                    line = re.sub('\*\*([^*]+)\*\*', fr'{self.ANSI_BOLD}\1{self.ANSI_RESET}', line)
            elif print_:
                line = f'{self.ANSI_GREEN}{line}{self.ANSI_RESET}'
            new_data.append(line)
        return '\n'.join(new_data)

    def md(self):
        """
        returning a Markdown file using Markdown features

        :return:    string of Markdown file
        :rtype:     str
        """
        return self._main_md()

    def print_md(self):
        """
        printing a Markdown file using Markdown features

        :rtype: None
        """
        os.system('')  # necessary for ANSI terminal printing
        print(self._main_md(print_=True))

    @classmethod
    def get_style(cls, style=None):
        style_dict = {
            'bold': cls.ANSI_BOLD,
            'underline': cls.ANSI_UNDERLINE,
            'italic': cls.ANSI_ITALIC,
            'yellow': cls.ANSI_YELLOW,
            'cyan': cls.ANSI_CYAN,
            'magenta': cls.ANSI_MAGENTA,
            'red': cls.ANSI_RED,
            'green': cls.ANSI_GREEN,
            'blue': cls.ANSI_BLUE
        }
        if (value:= style_dict.get(style)) is None:
            return cls.ANSI_RESET
        return value


class CSV(BaseFile):
    def __init__(self, encoded):
        super().__init__(encoded)
        self._table = str(self).split('\n')
        self._headers = list(self._table.pop(0).split(','))
        self.has_none = False
        for line in self._table:
            if len(line.split(',')) > len(self._headers):
                self.has_none = True

    def _full_csv(self):
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
            return self._full_csv()
        match [bool(type(row) is int and row > 0), type(col) is str and col in self._headers]:
            case [True, True]:
                return self._table[row-1].split(',')[self._headers.index(col)]
            case [True, False]:
                return self._table[row-1].split(',')
            case [False, True]:
                return {index+1: line.split(',')[self._headers.index(col)] for index, line in enumerate(self._table)}
            case [False, False]:
                self._raise(UnknownRowOrColumn)
        return None

    def print_csv(self, headers_color=None, lines_color=None, text_color=None):
        if not (self.__str__()):
            return
        if headers_color or lines_color or text_color:
            os.system('') # necessary for ANSI terminal printing

        rows = list(csv.reader(StringIO(self.__str__())))
        headers = rows.pop(0)
        raw_widths = []

        for i in range(len(headers)):
            max_w = len(headers[i])
            for row in rows:
                if i < len(row):
                    max_w = max(max_w, len(row[i]))
            raw_widths.append(max_w)
        col_widths = []
        base_padding = 2

        for i, w in enumerate(raw_widths):
            target_width = w + base_padding
            if (target_width - w) % 2 != 0:
                target_width += 1
            col_widths.append(target_width)

        def create_line(left, mid, right, fill):
            if lines_color:
                return (f'{Markdown.get_style(lines_color)}'
                        f'{left}{mid.join(fill * width for width in col_widths)}{right}'
                        f'{Markdown.ANSI_RESET}')
            return f'{left}{mid.join(fill * width for width in col_widths)}{right}'

        # adding color to headers
        if headers_color:
            headers = [(f'{Markdown.get_style(headers_color)}'
                        f'{h}'
                        f'{Markdown.ANSI_RESET}') for h in
                       [headers[i].center(col_widths[i]) for i in range(len(headers))]
                       ]
        else:
            headers = [headers[i].center(col_widths[i]) for i in range(len(headers))]

        #lines
        top_line = create_line('┏', '┳', '┓', '━')
        mid_line = create_line('┣', '╋', '┫', '━')
        bottom_line = create_line('┗', '┻', '┛', '━')

        #vertical seperator
        vs = f'{Markdown.get_style(lines_color)}┃{Markdown.ANSI_RESET}' if lines_color else '┃'


        # printing headers
        print(top_line)
        print(f"{vs}{vs.join(headers)}{vs}")
        print(mid_line)

        for row in rows:
            padded_data = row + [''] * (len(headers) - len(row))

            # adding text color
            if text_color:
                data_cells = [(f'{Markdown.get_style(text_color)}'
                               f'{r}'
                               f'{Markdown.ANSI_RESET}') for r in
                                [
                                  row[i].center(col_widths[i])
                                  if len(row) > i else (' '*col_widths[i])
                                  for i in range(len(headers))
                                ]
                              ]
            else:
                data_cells = [padded_data[i].center(col_widths[i]) for i in range(len(headers))]

            print(f"{vs}{vs.join(data_cells)}{vs}")

        print(bottom_line)