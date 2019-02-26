import sys
from termcolor import colored


class JsonOutputFormatter(object):
    def __init__(self, indent_spacer="  "):
        self._colored = self._dummy_colored
        self.indent_spacer_char = indent_spacer

        if sys.stdout.isatty():
            self._colored = colored

    def indent_spacer(self, num):
        return self.indent_spacer_char * num

    @staticmethod
    def _dummy_colored(string, *args, **kwargs):
        return string

    def print_obj(self, data, indent=0):
        if isinstance(data, dict):
            self._write('{\n')
            self.print_dict(data, indent + 1)
            self._write(self.indent_spacer(indent))
            self._write('}\n')
        elif isinstance(data, str):
            self._write('"{}",\n'.format(data))
        elif isinstance(data, list):
            self._write('[{}],\n'.format(", ".join(data)))
        elif isinstance(data, tuple):
            self._write('{},\n'.format(data))
        else:
            self._write('{},\n'.format(data))

    def print_dict(self, data, indent=0):
        keys = list(data.keys())
        keys.sort()

        for k in keys:
            v = data[k]
            self._write(self.indent_spacer(indent))
            self._write('"{}"'.format(k), 'blue')
            self._write(': ')
            self.print_obj(v, indent)

    def print_header(self, data):
        self._write(data + '\n', attrs=['bold'])

    def println(self, *data, indent=0):
        self._write(self.indent_spacer(indent))
        self._write(" ".join(data) + '\n')

    def print_pair(self, k, data, indent=0):
        self._write(self.indent_spacer(indent))
        self._write(k, 'blue')
        self._write(': ')
        self._write(data)
        self._write('\n')

    def _write(self, string, *args, **kwargs):
        print(self._colored(string, *args, **kwargs), end='')