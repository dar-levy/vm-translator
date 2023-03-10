class CodeGenerator:
    def __init__(self):
        self.current_function = ""
        self.nextLabel = 0
        self.bootstrap = ["@256", "D=A", "@SP", "M=D"]
        self.arithmetics = {
            "add": ["@SP",
                    "A=M",
                    "A=A-1",
                    "A=A-1",
                    "D=M",
                    "A=A+1",
                    "D=D+M",
                    "@SP",
                    "M=M-1",
                    "M=M-1",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1"],
            "sub": ["@SP",
                    "A=M",
                    "A=A-1",
                    "A=A-1",
                    "D=M",
                    "A=A+1",
                    "D=D-M",
                    "@SP",
                    "M=M-1",
                    "M=M-1",
                    "A=M",
                    "M=D",
                    "@SP",
                    "M=M+1"],
            "neg": ["@SP", "A=M-1", "M=-M"],
        }
        self.comparisons = {
            "eq": (lambda label: ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", "@eqTrue" + label, "D;JEQ",
                                  "@SP", "A=M-1", "M=0", "(eqTrue" + label + ")"]),
            "gt": (lambda label: ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", "@gtTrue" + label, "D;JGT",
                                  "@SP", "A=M-1", "M=0", "(gtTrue" + label + ")"]),
            "lt": (lambda label: ["@SP",
                                  "A=M",
                                  "A=A-1",
                                  "A=A-1",
                                  "D=M",
                                  "A=A+1",
                                  "D=D-M",
                                  "@SP",
                                  "M=M-1",
                                  "M=M-1",
                                  f"@TRUE{label}",
                                  "D;JLT",
                                  "@SP",
                                  "A=M",
                                  "M=0",
                                  f"@END{label}",
                                  "0;JMP",
                                  f"(TRUE{label})",
                                  "@SP",
                                  "A=M",
                                  "M=-1",
                                  f"(END{label})",
                                  "@SP",
                                  "M=M+1"
                                  ])
        }
        self.logics = {
            "not": ["@SP", "A=M-1", "M=!M"],
            "or": ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "M=D|M"],
            "and": ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "M=D&M"]
        }
        self.push = {
            "constant": (lambda index: [
                "@" + index,
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ]),
            "static": (lambda index: [
                f"@{self.current_function.split('.')[0]}.{index}",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]),
            "this": (lambda index: [
                "@" + index,
                "D=A",
                "@THIS",
                "A=M+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]),
            "that": (lambda index: [
                "@" + index,
                "D=A",
                "@THAT",
                "A=M+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]),
            "argument": (lambda index: [
                "@" + index,
                "D=A",
                "@ARG",
                "A=M",
                "D=D+A",
                "A=D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]),
            "local": (lambda index: [
                "@" + index,
                "D=A",
                "@LCL",
                "A=M+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]),
            "temp": (lambda index: [
                "@" + index,
                "D=A",
                "@5",
                "A=A+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ]),
            "pointer": (lambda index: [
                "@" + index,
                "D=A",
                "@3",
                "A=A+D",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ])
        }
        self.pop = {
            "static": (lambda index: [
                "@SP",
                "AM=M-1",
                "D=M",
                f"@{self.current_function.split('.')[0]}.{index}",
                "M=D"
            ]),
            "this": (lambda index: [
                "@" + index,
                "D=A",
                "@THIS",
                "D=M+D",
                "@R13",
                "M=D",
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D"
            ]),
            "that": (lambda index: [
                "@" + index,
                "D=A",
                "@THAT",
                "D=M+D",
                "@R13",
                "M=D",
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D"
            ]),
            "argument": (lambda index: [
                "@" + index,
                "D=A",
                "@ARG",
                "D=M+D",
                "@R13",
                "M=D",
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D"
            ]),
            "local": (lambda index: [
                "@" + index,
                "D=A",
                "@LCL",
                "D=M+D",
                "@R13",
                "M=D",
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D"
            ]),
            "pointer": (lambda index: [
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@THAT",
                "M=D"
            ]),
            "temp": (lambda index: [
                "@" + index,
                "D=A",
                "@5",
                "D=A+D",
                "@R13",
                "M=D",
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
                "M=D"
            ])
        }
        self.branching = {
            "label": (lambda expression: [
                f"({self.current_function}${expression})",
            ]),
            "goto": (lambda expression: [
                f"@{self.current_function}${expression}",
                "0;JMP"
            ]),
            "if-goto": (lambda expression: [
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                f"@{self.current_function}${expression}",
                "D;JNE"
            ]),
        }
        self.functions = {
            "function": (lambda function_name, line_number: [
                f"({function_name[1]})",
            ]),
            "function_extension": (lambda function_name, line_number: [
                "@SP",
                "A=M",
                "M=0",
                "@SP",
                "M=M+1",
            ]),
            "return": (lambda function_name, line_number: [
                "@LCL",
                "D=M",
                "@frame",
                "M=D",
                "@5",
                "D=D-A",
                "A=D",
                "D=M",
                "@ret",
                "M=D",
                "@SP",
                "M=M-1",
                "A=M",
                "D=M",
                "@ARG",
                "A=M",
                "M=D",
                "@ARG",
                "D=M+1",
                "@SP",
                "M=D",
                "@frame",
                "D=M",
                "@1",
                "D=D-A",
                "A=D",
                "D=M",
                "@THAT",
                "M=D",
                "@frame",
                "D=M",
                "@2",
                "D=D-A",
                "A=D",
                "D=M",
                "@THIS",
                "M=D",
                "@frame",
                "D=M",
                "@3",
                "D=D-A",
                "A=D",
                "D=M",
                "@ARG",
                "M=D",
                "@frame",
                "D=M",
                "@4",
                "D=D-A",
                "A=D",
                "D=M",
                "@LCL",
                "M=D",
                "@ret",
                "A=M",
                "0;JMP"
            ]),
            "call": (lambda function_name, line_number: [
                f"@RETURN{line_number}",
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                "@LCL",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                "@ARG",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                "@THIS",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                "@THAT",
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
                "D=M",
                f"@{function_name[2]}",
                "D=D-A",
                "@5",
                "D=D-A",
                "@ARG",
                "M=D",
                "@SP",
                "D=M",
                "@LCL",
                "M=D",
                f"@{function_name[1]}",
                "0;JMP",
                f"(RETURN{line_number})"
            ])
        }

    def get_bootstrap(self):
        return self.bootstrap

    def get_functions_handle(self, handle, subexpressions, line_number):
        assembly_function = self.functions[handle](subexpressions, line_number)
        if handle == "function":
            self.current_function = subexpressions[1]
            for i in range(int(subexpressions[2])):
                assembly_function = assembly_function + self.functions["function_extension"]("extension", 1)

        return assembly_function

    def get_branching_command(self, command, expression):
        return self.branching[command](expression)

    def get_arithmetic_gate(self, command):
        return self.arithmetics[command]

    def get_logic_gate(self, command):
        return self.logics[command]

    def get_comparison_gate(self, command):
        label = str(self.nextLabel)
        self.nextLabel += 1
        return self.comparisons[command](label)

    def get_push_segment(self, segment, index):
        return self.push[segment](index)

    def get_pop_segment(self, segment, index):
        return self.pop[segment](index)
