import argparse
from itertools import tee
import json
import re

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('input_file', type=str, help='Input file path')
parser.add_argument('-o', '--output_file', type=str, help='Output file path')
args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file

if not output_file:
    output_file = input_file + ".s"

class Peekable:
    def __init__(self, it):
        self.it = it

    def peek(self):
        current, backup = tee(self.it)
        self.it = backup
        try:
            return next(current)
        except StopIteration:
            return None
    
    def __next__(self):
        try:
            return next(self.it)
        except StopIteration:
            return None

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

used_regs = 0

def parse_type(tokens):
    t = next(tokens)
    if t[0] != Token.TYPE:
        raise RuntimeException(f"{t} not a type")
    return None if t[1] == "void" else t[1]

def parse_constant(tokens):
    global used_regs
    t = next(tokens)
    if t[0] != Token.VALUE:
        raise RuntimeException(f"{t} is not a constant")
    r = used_regs
    used_regs += 1
    return {"op": "const", "type": "int", "dest": f"r{r}", "value": t[1]}

def parse_expression(tokens):
    global used_regs
    instrs = []
    instrs.append(parse_constant(tokens))
    if tokens.peek()[0] == Token.ADD:
        left = instrs[-1]["dest"]
        next(tokens)
        out, ins = parse_expression(tokens)
        instrs += ins
        right = instrs[-1]["dest"]
        r = used_regs
        used_regs += 1
        instrs.append({"op": "add", "dest": f"r{r}", "args":[left, right]})
    if len(instrs):
        out = instrs[-1]["dest"]
    else:
        out = None
    return out, instrs

def parse_statement(tokens):
    instrs = []
    t = next(tokens)
    if t[0] == Token.RET:
        out, ins = parse_expression(tokens)
        instrs = ins
        instrs.append({
            "op":"ret",
            "args": out
            })
    elif t[0] == Token.SEMI:
        return instrs
    if next(tokens)[0] != Token.SEMI:
        raise RuntimeException(f"{t} not ;")
    return instrs

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
    instrs = []
    while tokens.peek()[0] != Token.RBRA:
        instrs += parse_statement(tokens)
    if next(tokens)[0] != Token.RBRA:
        raise RuntimeException(f"{t} not right bracket")
    return {
            "name": name[1],
            "type": t,
            "args": [],
            "instrs": instrs
            }

def parse_program(tokens):
    functions = []
    while tokens.peek():
        functions.append(parse_function(tokens))
    return {
            "functions": functions
            }

contents = read_file(input_file)
tokens = tokenize(contents)
ir = parse_program(Peekable(iter(tokens)))
print(json.dumps(ir))
