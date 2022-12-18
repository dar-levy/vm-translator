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

    def hasMoreCommands(self):
        position = self.infile.tell()
        self.advance()
        self.infile.seek(position)
        return not self.advanceReachedEOF

    def advance(self):
        thisLine = self.infile.readline()
        if thisLine == '':
            self.advanceReachedEOF = True
        else:
            splitLine = thisLine.split("/")[0].strip()
            if splitLine == '':
                self.advance()
            else:
                self.command = splitLine.split()
