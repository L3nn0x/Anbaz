import re

class Token:
    TYPE = "type"
    NAME = "name"
    RET = "return"
    LPAR = "left parenthesis"
    RPAR = "right parenthesis"
    LBRA = "left bracket"
    RBRA = "right bracket"
    SEMI = "semicolumn"
    VALUE = "value"
    ADD = "add"

def read_file(name):
    with open(name, "r") as fp:
        return fp.read()

types = {"int", "void"}

def tokenize(contents):
    c = (i for i in contents.split() if i)
    cc = []
    tokens = []
    for i in c:
        tmp = re.split("([\(\){};+])", i)
        cc += tmp
    for tok in cc:
        if not tok:
            continue
        if tok in types:
            tokens.append((Token.TYPE, tok))
        elif tok == '(':
            tokens.append((Token.LPAR, None))
        elif tok == ')':
            tokens.append((Token.RPAR, None))
        elif tok == '{':
            tokens.append((Token.LBRA, None))
        elif tok == '}':
            tokens.append((Token.RBRA, None))
        elif tok == ';':
            tokens.append((Token.SEMI, None))
        elif tok == 'return':
            tokens.append((Token.RET, None))
        elif tok == '+':
            tokens.append((Token.ADD, None))
        elif tok.isdigit():
            tokens.append((Token.VALUE, int(tok)))
        else:
            tokens.append((Token.NAME, tok))
    return tokens
