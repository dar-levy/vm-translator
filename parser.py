class Parser:
    def __init__(self):
        self.cType = {
            "sub": "math",
            "add": "math",
            "neg": "math",
            "eq": "math",
            "gt": "math",
            "lt": "math",
            "and": "math",
            "or": "math",
            "not": "math",
            "push": "push",
            "pop": "pop",
            "EOF": "EOF",
        }

    def commandType(self):
        return self.cType.get(self.command[0], "invalid cType")

    def arg1(self):
        return self.command[1]

    def arg2(self):
        return self.command[2]
