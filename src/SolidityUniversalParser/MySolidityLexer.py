from antlr4.error.ErrorStrategy import DefaultErrorStrategy

from src.resource.antlr4.myParser.SolidityLexer import SolidityLexer


class MySolidityLexer (SolidityLexer):
    def recover(self, e):
        return
