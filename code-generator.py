class CodeWriter:
    def __init__(self, dest):
        self.root = dest[:-4].split('/')[-1]
        self.outfile = open(dest, "w")
        self.nextLabel = 0

    def setFileName(self, source):
        self.fileName = source[:-3]

    def writeArithmetic(self, command):
        trans = ""
        if command == "add":
            trans += "@SP\n"  # pop first value into D
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"  # pop second value into M
            trans += "AM=M-1\n"
            trans += "M=D+M\n"  # push sum onto M
            trans += "@SP\n"
            trans += "M=M+1\n"
        elif command == "sub":
            trans += "@SP\n"  # pop first value into D
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"  # pop second value into M
            trans += "AM=M-1\n"
            trans += "M=M-D\n"  # push difference onto M
            trans += "@SP\n"
            trans += "M=M+1\n"
        elif command == "neg":
            trans += "@SP\n"  # get (not pop) value into M
            trans += "A=M-1\n"
            trans += "M=-M\n"  # and negate it
        elif command == "not":
            trans += "@SP\n"  # get (not pop) value into M
            trans += "A=M-1\n"
            trans += "M=!M\n"  # and negate it
        elif command == "or":
            trans += "@SP\n"  # pop first value into D
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"  # get second value into M
            trans += "A=M-1\n"
            trans += "M=D|M\n"  # put result back on stack
        elif command == "and":
            trans += "@SP\n"  # pop first value into D
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"  # get second value into M
            trans += "A=M-1\n"
            trans += "M=D&M\n"  # put result back on stack
        elif command == "eq":
            label = str(self.nextLabel)
            self.nextLabel += 1
            trans += "@SP\n"  # pop first value into D
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"  # get second value into M
            trans += "A=M-1\n"
            trans += "D=M-D\n"  # D = older value - newer
            trans += "M=-1\n"  # tentatively put true on stack
            trans += "@eqTrue" + label + "\n"  # and jump to end if so
            trans += "D;JEQ\n"
            trans += "@SP\n"  # set to false otherwise
            trans += "A=M-1\n"
            trans += "M=0\n"
            trans += "(eqTrue" + label + ")\n"
        elif command == "gt":
            label = str(self.nextLabel)
            self.nextLabel += 1
            trans += "@SP\n"  # pop first value into D
            trans += "AM=M-1\n"
            trans += "D=M\n"
            trans += "@SP\n"  # get second value into M
            trans += "A=M-1\n"
            trans += "D=M-D\n"  # D = older value - newer
            trans += "M=-1\n"  # tentatively put true on stack
            trans += "@gtTrue" + label + "\n"  # and jump to end if so
            trans += "D;JGT\n"
            trans += "@SP\n"  # set to false otherwise
            trans += "A=M-1\n"
            trans += "M=0\n"
            trans += "(gtTrue" + label + ")\n"
        elif command == "lt":
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
        else:
            trans = command + " not implemented yet\n"
        self.outfile.write("// " + command + "\n" + trans)
