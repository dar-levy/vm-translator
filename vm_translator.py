import os

from parser import Parser


class VMTranslator:
    def __init__(self, input_file_path):
        self.parser = Parser()
        self.binary_file_content = []
        self.file_content = self._read_file(input_file_path)
        self.output_file_path = os.path.splitext(input_file_path)[0] + '.hack'

    def assemble(self):
        self._clean_file()
        self._add_label_symbols_to_table()
        self._convert_to_binary()
        self._write_to_file()

    def _clean_file(self):
        self.file_content = [line.split('/')[0].strip() for line in self.file_content if
                             line.strip() != '' and line.split('/')[0].strip() != '']

    def _add_label_symbols_to_table(self):
        labels = []
        for line_number, line in enumerate(self.file_content):
            if '(' in line:
                self.parser.parse(line, line_number - len(labels))
                labels.append(line)

        self.file_content = [line for line in self.file_content if line not in labels]

    def _convert_to_binary(self):
        for line_num, line in enumerate(self.file_content):
            binary_line = self.parser.parse(line, line_num)
            self.binary_file_content.append(binary_line)

    def _read_file(self, file_path):
        with open(file_path, "r") as input_file:
            lines = input_file.read().splitlines()

        input_file.close()
        return lines

    def _write_to_file(self):
        with open(self.output_file_path, 'w') as output_file:
            output_file.write('\n'.join(self.binary_file_content))

        output_file.close()
