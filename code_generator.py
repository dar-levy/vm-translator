class CodeGenerator:
    def __init__(self, root):
        self.nextLabel = 0
        self.arithmetics = {
            "add": ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "M=M+D", "@SP", "M=M+1"],
            "sub": ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "M=M-D", "@SP", "M=M+1"],
            "neg": ["@SP", "A=M-1", "M=-M"],
        }
        self.comparisons = {
            "eq": (lambda label: ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", "@eqTrue" + label, "D;JEQ",
                                  "@SP", "A=M-1", "M=0", "(eqTrue" + label + ")"]),
            "gt": (lambda label: ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", "@gtTrue" + label, "D;JGT",
                                  "@SP", "A=M-1", "M=0", "(gtTrue" + label + ")"]),
            "lt": (lambda label: ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", "@ltTrue" + label, "D;JLT",
                                  "@SP", "A=M-1", "M=0", "(ltTrue" + label + ")"])
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
                "@" + root + "." + index,
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
                "A=M+D",
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
                "@" + root + "." + index,
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
                "@" + index,
                "D=A",
                "@3",
                "D=A+D",
                "@R13",
                "M=D",
                "@SP",
                "AM=M-1",
                "D=M",
                "@R13",
                "A=M",
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

    def get_arithmetic_gate(self, command):
        return self.arithmetics[command]

    def get_logic_gate(self, command):
        return self.arithmetics[command]

    def get_comparison_gate(self, command):
        label = str(self.nextLabel)
        self.nextLabel += 1
        return self.comparisons[command](label)

    def get_push_segment(self, segment, index):
        return self.push[segment](index)

    def get_pop_segment(self, segment, index):
        return self.pop[segment](index)
