from code_generator import CodeGenerator


class Parser:
    def __init__(self, root):
        self.code_generator = CodeGenerator(root)
        self.arithmetics = list(self.code_generator.arithmetics.keys())
        self.comparisons = list(self.code_generator.comparisons.keys())
        self.logics = list(self.code_generator.logics.keys())
        self.push = list(self.code_generator.push.keys())
        self.pop = list(self.code_generator.pop.keys())

    def parse(self, expression, index):
        subexpressions = expression.split(' ')
        command = subexpressions[0]
        if command in self.arithmetics:
            return self.arithmetics[command]
        elif command in self.comparisons:
            return self.comparisons[command](index)
        elif command in self.logics:
            return self.logics[command]
        elif command in self.push:
            return self.push[command](index)
        elif command in self.pop:
            return self.pop[command](index)
