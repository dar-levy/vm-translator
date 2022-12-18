import sys
from parser import Parser
from code_generator import CodeGenerator


def main():
    root = sys.argv[1]
    parser = Parser(root + ".vm")
    writer = CodeGenerator(root + ".asm")

    while parser.hasMoreCommands():
        parser.advance()
        cType = parser.commandType()
        if cType == "push" or cType == "pop":
            writer.writePushPop(cType, parser.arg1(), parser.arg2())
        elif cType == "math":
            writer.writeArithmetic(parser.command[0])
        else:
            writer.writeError()


if __name__ == '__main__':
    main()
