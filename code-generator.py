class CodeWriter:
    def __init__(self, dest):
        self.root = dest[:-4].split('/')[-1]
        self.outfile = open(dest, "w")
        self.nextLabel = 0

    def setFileName(self, source):
        self.fileName = source[:-3]
