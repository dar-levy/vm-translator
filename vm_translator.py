import os

from parser import Parser


class VMTranslator:
    def __init__(self, input_file_path):
        self.parser = Parser()
        self.assembly_file_content = []
        self.file_content = self._read_file(input_file_path)
        self.output_file_path = os.path.splitext(input_file_path)[0] + '.hack'

    def translate(self):
        self._clean_file()
        self._convert_to_assembly()
        self._write_to_file()

    def _clean_file(self):
        self.file_content = [line.split('/')[0].strip() for line in self.file_content if
                             line.strip() != '' and line.split('/')[0].strip() != '']

    def _convert_to_assembly(self):
        for line_num, line in enumerate(self.file_content):
            assembly_translation = self.parser.parse(line, line_num)
            self.assembly_file_content.extend(assembly_translation)

    def _read_file(self, file_path):
        with open(file_path, "r") as input_file:
            lines = input_file.read().splitlines()

        input_file.close()
        return lines

    def _write_to_file(self):
        with open(self.output_file_path, 'w') as output_file:
            output_file.write('\n'.join(self.binary_file_content))

        output_file.close()