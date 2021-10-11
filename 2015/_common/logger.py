# -*- coding: utf-8 -*-
INDENTATION_CONSTANT = 2

class Logger:
    outpath: str
    loglines: [str]
    indentation: int

    def __init__(self, outpath):
        self.outpath = outpath
        self.loglines = []
        self.indentation = 0

    def indent(self, amount=1):
        self.indentation += amount

    def unindent(self, amount=1):
        self.indent(amount*(-1))

    def getIndent(self) -> str:
        return " " * INDENTATION_CONSTANT * self.indentation

    def print(self, msg: str = ""):
        print(self.getIndent() + msg)

    def log(self, msg: str = ""):
        self.loglines.append(self.getIndent() + msg)

    def tee(self, msg: str = ""):
        self.log(msg)
        print(msg)

    def dmp(self):
        self.print()
        with open(self.outpath, "w") as outfile:
            outtext: str = "\n".join(self.loglines)
            outfile.write(outtext)
            self.print(f"Successfully dumped logs to {self.outpath}!")
