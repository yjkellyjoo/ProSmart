from antlr4.error.ErrorStrategy import DefaultErrorStrategy

from .SolidityLexer import SolidityLexer


class MySolidityLexer (SolidityLexer):
    def recover(self, e):
        return
