import hashlib

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from src.SolidityUniversalParser.MySolidityVisitor import MySolidityVisitor, VisitSolidityListener
from src.SolidityUniversalParser.SolidityLexer import SolidityLexer as MySolidityLexer
from src.SolidityUniversalParser.SolidityParser import SolidityParser as MySolidityParser

from src import constants as const


def run_vccd(code):
    lexer = MySolidityLexer(InputStream(code))
    tokens = lexer.getAllTokens()

    lexer.reset()
    visitor = MySolidityVisitor()
    parser = MySolidityParser(CommonTokenStream(lexer))
    result_map = visitor.visit(parser.contractPart())

    ## make string list of tokens
    token_list = []
    for token in tokens:
        ## abstract function visibility
        ## public(external)인지 private인지 구분하는게 오히려 중요한 부분. public, external과 empty를 동일시 해준다.
        if token.type == lexer.PublicKeyword or token.type == lexer.ExternalKeyword:
            continue
        else:
            token_list.append(token.text)

    ## abstract 'emit' keyword: remove 'emit' keyword
    while 'emit' in token_list:
        token_list.remove('emit')

    ## abstract type conversions (esp. address types).
    walker = ParseTreeWalker()
    listener = VisitSolidityListener()
    lexer.reset()
    parser.reset()
    walker.walk(listener, parser.contractPart())
    converted_variables = listener.type_conversion_strings

    ## abstraction
    token_list = abstract(token_list, result_map[const.funccall], const.funccall)    ## fparam can be used as a funccall. it must be replaced before fparam.
    token_list = abstract(token_list, result_map[const.fparam], const.fparam)
    token_list = abstract(token_list, converted_variables, const.lvar)              ## dtype can be part of type conversion. Must be done before abstracting data types.
    token_list = abstract(token_list, result_map[const.dtype], const.dtype)
    token_list = abstract(token_list, result_map[const.eventcall], const.funccall)
    token_list = abstract(token_list, result_map[const.lvar], const.lvar)

    ## abstract return
    abst_code = ""
    for token in token_list:
        abst_code += (token + " ")
    abst_code = abst_code.lower()
    sha3hash = hashlib.sha256(abst_code.encode())

    return sha3hash.hexdigest()


def abstract(token_list, ids, replace_const):
    for _id in ids:
        if type(_id) == str:
            _id = [_id]

        id_len = len(_id)
        for i in range(len(token_list) - id_len+1):
            cmp = token_list[i:i+id_len]
            if _id == cmp:
                token_list[i:i+id_len] = [replace_const]

    return token_list


