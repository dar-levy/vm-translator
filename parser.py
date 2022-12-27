from code_generator import CodeGenerator


class Parser:
    def __init__(self, root):
        self.code_generator = CodeGenerator(root)
        self.arithmetics = list(self.code_generator.arithmetics.keys())
        self.comparisons = list(self.code_generator.comparisons.keys())
        self.branching = list(self.code_generator.branching.keys())
        self.logics = list(self.code_generator.logics.keys())

    def parse(self, expression):
        subexpressions = expression.split()
        command = subexpressions[0]
        if command in self.logics:
            return self.code_generator.get_logic_gate(command)
        elif command in self.arithmetics:
            return self.code_generator.get_arithmetic_gate(command)
        elif command in self.comparisons:
            return self.code_generator.get_comparison_gate(command)
        elif command in self.branching:
            return self.code_generator.get_branching_command(command, expression[1])
        elif command == "push":
            return self.code_generator.get_push_segment(subexpressions[1], subexpressions[2])
        elif command == "pop":
            return self.code_generator.get_pop_segment(subexpressions[1], subexpressions[2])
