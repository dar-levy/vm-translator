import os
from parser import Parser


class VMTranslator:
    def __init__(self, directory_path):
        self.content = []
        self.assembly_content = []
        self.input_path = directory_path
        self.output_file_path = directory_path + '.asm'
        self.parser = Parser(os.path.basename(os.path.normpath(directory_path)))

    def translate(self):
        self._bootstrap()
        self._convert_to_assembly()
        self._write_to_file()

    def _bootstrap(self):
        self._read_directory()
        self._clean_content()
        self._bootstrap_assembly_content()

    def _bootstrap_assembly_content(self):
        init_function_name = ''.join([line.split()[1] for line in self.content if ".init" in line])
        if init_function_name:
            bootstrap_prefix = ["// bootstrap"] + self.parser.parse("bootstrap") + [""]
            bootstrap_suffix = [f"// call {init_function_name}"] + self.parser.parse(f"call {init_function_name}",
                                                                                     "bootstrap") + [""]
            self.assembly_content = bootstrap_prefix + bootstrap_suffix

    def _clean_content(self):
        self.content = [line.split('/')[0].strip() for line in self.content if
                        line.strip() != '' and line.split('/')[0].strip() != '']

    def _convert_to_assembly(self):
        for line_number, line in enumerate(self.content):
            assembly_translation = self.parser.parse(line, line_number + 1)
            self.assembly_content.extend(["// " + line])
            self.assembly_content.extend(assembly_translation)
            self.assembly_content.extend([""])

    def _read_directory(self):
        for file in os.listdir(self.input_path):
            if file.endswith(".vm"):
                content = self._read_file(os.path.join(self.input_path, file))
                self.content.extend(content)

    def _read_file(self, file_path):
        with open(file_path, "r") as input_file:
            lines = input_file.read().splitlines()

        input_file.close()
        return lines

    def _write_to_file(self):
        with open(self.output_file_path, 'w') as output_file:
            output_file.write('\n'.join(self.assembly_content))

        output_file.close()
