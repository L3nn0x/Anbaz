import argparse
import json

from .peekable import Peekable
from .lexer import read_file, tokenize
from .parser import parse_translation_unit
from .ir import GenerateIr

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('input_file', type=str, help='Input file path')
parser.add_argument('-o', '--output_file', type=str, help='Output file path')
args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file

if not output_file:
    output_file = input_file + ".s"

contents = read_file(input_file)
tokens = tokenize(contents)
ast = parse_translation_unit(Peekable(iter(tokens)))
irv = GenerateIr()
ast.visit(irv)
print(json.dumps(irv.generate()))
