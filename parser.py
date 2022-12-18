class Parser:
    def __init__(self, source):
        self.infile = open(source)
        self.command = ["nada"]
        self.advanceReachedEOF = False

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
