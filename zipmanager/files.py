import os
import re

class Markdown(str):
    def __main_md(self, print_=False):
        new_data = []
        is_code = False
        under_line = '\u001b[4m'
        end = '\u001b[0m'
        for line in self.split('\n'):
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