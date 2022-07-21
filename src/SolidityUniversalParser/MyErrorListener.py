from antlr4.error.ErrorListener import ErrorListener


class MyErrorListener(ErrorListener):
    def __init__(self):
        self.errorBool = False

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if e is not None:
            print(type(e))
            self.errorBool = True

    def getErrorStatus(self):
        return self.errorBool
