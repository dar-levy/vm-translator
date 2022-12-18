class CodeGenerator:
    def __init__(self, dest):
        self.root = dest[:-4].split('/')[-1]
        self.outfile = open(dest, "w")
        self.nextLabel = 0
        self.arithmetics = {
            "add": ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "M=D+M", "@SP", "M=M+1"],
            "sub": ["@SP", "AM=M-1", "D=M", "@SP", "AM=M-1", "M=D-M", "@SP", "M=M+1"],
            "neg": ["@SP", "A=M-1", "M=-M"],
            "not": ["@SP", "A=M-1", "M=!M"],
            "or": ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "M=D|M"],
            "and": ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "M=D&M"],
            "eq": ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", "@eqTrue" + label, "D;JEQ",
                   "@SP", "A=M-1", "M=0", "(eqTrue" + label + ")"],
            "gt": ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", "@gtTrue" + label, "D;JGT",
                   "@SP", "A=M-1", "M=0", "(gtTrue" + label + ")"],
            "lt": ["@SP", "AM=M-1", "D=M", "@SP", "A=M-1", "D=M-D", "M=-1", "@ltTrue" + label, "D;JLT",
                   "@SP", "A=M-1", "M=0", "(ltTrue" + label + ")"]
        }
        self.push = {
            "constant": [
                "@" + index,
                "D=A",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1",
            ],
            "static": [
                "@" + self.root + "." + index,
                "D=M",
                "@SP",
                "A=M",
                "M=D",
                "@SP",
                "M=M+1"
            ],
            "this": [
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
            ],
            "that": [
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
            ],
            "argument": [
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
            ],
            "local": [
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
            ],
            "temp": [
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
            ],
            "pointer": [
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
            ]
        }
        self.pop = {
            "static": [
                "@SP",
                "AM=M-1",
                "D=M",
                "@" + self.root + "." + index,
                "M=D"
            ],
            "this": [
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
            ],
            "that": [
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
            ],
            "argument": [
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
            ],
            "local": [
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
            ],
            "pointer": [
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
            ],
            "temp": [
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
            ]
        }

    def writeArithmetic(self, command):
        trans = ""
        if command == "lt":
            label = str(self.nextLabel)
            self.nextLabel += 1
            trans += "@SP\n"  # pop first value into D
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"  # get second value into M
            trans += "A=M-1\n"
            trans += "D=M-D\n"  # D = older value - newer
            trans += "M=-1\n"  # tentatively put true on stack
            trans += "@ltTrue" + label + "\n"  # and jump to end if so
            trans += "D;JLT\n"
            trans += "@SP\n"  # set to false otherwise
            trans += "A=M-1\n"
            trans += "M=0\n"
            trans += "(ltTrue" + label + ")\n"

    def writeError(self):
        self.outfile.write("Whoopsie, command not recognized\n")
