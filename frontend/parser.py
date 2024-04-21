from .lexer import Token

class Node:
    def visit(self, visitor):
        pass

class Type(Node):
    def __init__(self, t):
        self.t = t

    def visit(self, visitor):
        visitor.visit_type(self)

class Const(Node):
    def __init__(self, value, value_type=Type("int")):
        self.value = value
        self.value_type = value_type

    def visit(self, visitor):
        self.value_type.visit(visitor)
        visitor.visit_const(self)

class Return(Node):
    def __init__(self, expr):
        self.expr = expr

    def visit(self, visitor):
        self.expr.visit(visitor)
        visitor.visit_return(self)

class StatementList(Node):
    def __init__(self, statements):
        self.statements = statements

    def visit(self, visitor):
        for s in self.statements:
            s.visit(visitor)

class Function(Node):
    def __init__(self, ret_type, name, args, statements):
        self.ret_type = ret_type
        self.name = name
        self.args = args
        self.statements = statements

    def visit(self, visitor):
        self.statements.visit(visitor)
        visitor.visit_type(self.ret_type)
        visitor.visit_function(self)

class TranslationUnit(Node):
    def __init__(self, functions):
        self.functions = functions

    def visit(self, visitor):
        for function in self.functions:
            function.visit(visitor)

def parse_type(tokens):
    t = next(tokens)
    if t[0] != Token.TYPE:
        raise RuntimeException(f"{t} not a type")
    return Type(t[1])

def parse_constant(tokens):
    t = next(tokens)
    if t[0] != Token.VALUE:
        raise RuntimeException(f"{t} is not a constant")
    return Const(t[1])

def parse_expression(tokens):
    return parse_constant(tokens)

def parse_statement(tokens):
    t = next(tokens)
    ret = None
    if t[0] == Token.RET:
        ret = Return(parse_expression(tokens))
    if next(tokens)[0] != Token.SEMI:
        raise RuntimeException(f"{t} not ;")
    return ret

def parse_function(tokens):
    t = parse_type(tokens)
    name = next(tokens)
    if name[0] != Token.NAME:
        raise RuntimeException("no function name")
    if next(tokens)[0] != Token.LPAR:
        raise RuntimeException(f"{t} not left parenthesis")
    # parse args
    if next(tokens)[0] != Token.RPAR:
        raise RuntimeException(f"{t} not right parenthesis")
    if next(tokens)[0] != Token.LBRA:
        raise RuntimeException(f"{t} not left bracket")
    # parse statements
    statements = []
    while tokens.peek()[0] != Token.RBRA:
        statements.append(parse_statement(tokens))
    if next(tokens)[0] != Token.RBRA:
        raise RuntimeException(f"{t} not right bracket")
    return Function(t, name[1], [], StatementList(statements))

def parse_translation_unit(tokens):
    functions = []
    while tokens.peek():
        functions.append(parse_function(tokens))
    return TranslationUnit(functions)
