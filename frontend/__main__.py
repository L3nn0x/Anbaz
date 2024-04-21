import argparse
import json

from .peekable import Peekable
from .lexer import read_file, tokenize
from .parser import parse_translation_unit
from .ir import GenerateIr

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('input_file', type=str, help='Input file path')
parser.add_argument('-o', '--output_file', type=str, help='Output file path')
parser.add_argument('-p', '--print_ast', action='store_true', help='prints the ast then exits')
args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file

if not output_file:
    output_file = input_file + ".s"

class PrintVisitor:
    def __init__(self):
        self.current_type = None
        self.current_expr = None
        self.body = ""

    def visit_type(self, t):
        self.current_type = t.t

    def visit_const(self, c):
        self.current_expr = f"const_{self.current_type}({c.value})"

    def visit_return(self, r):
        self.body += f"\treturn {'' if not self.current_expr else self.current_expr}\n"
        self.current_expr = None

    def visit_function(self, f):
        print(f"function {self.current_type} {f.name}:")
        print(f"args: {f.args}")
        print(self.body)

contents = read_file(input_file)
tokens = tokenize(contents)
ast = parse_translation_unit(Peekable(iter(tokens)))
if args.print_ast:
    p = PrintVisitor()
    ast.visit(p)
else:
    irv = GenerateIr()
    ast.visit(irv)
    print(json.dumps(irv.generate()))
