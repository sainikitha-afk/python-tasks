from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

code = """
let x = 10
let y = 20
print x + y
"""

tokens = tokenize(code)

print("=== Lexer Output ===")
print(tokens)

parser = Parser(tokens)
ast = parser.parse()

print("\n=== Interpreter Output ===")
interpreter = Interpreter()

for stmt in ast:
    interpreter.eval(stmt)