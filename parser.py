from code_generator import CodeGenerator


class Parser:
    def __init__(self, root):
        self.code_generator = CodeGenerator(root)
        self.arithmetics = list(self.code_generator.arithmetics.keys())
        self.comparisons = list(self.code_generator.comparisons.keys())
        self.logics = list(self.code_generator.logics.keys())

    def parse(self, expression, index):
        subexpressions = expression.split()
        command = subexpressions[0]
        segment = subexpressions[1]
        value = subexpressions[2]
        if command in self.logics:
            return self.code_generator.logics[command]
        elif command in self.arithmetics:
            return self.code_generator.arithmetics[command]
        elif command in self.comparisons:
            return self.code_generator.comparisons[command]
        elif command == "push":
            return self.code_generator.push[segment](value)
        elif command == "pop":
            return self.code_generator.pop[segment](value)
