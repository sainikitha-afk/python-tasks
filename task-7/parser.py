from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def eat(self):
        self.pos += 1

    def parse_number(self):
        val = self.current()[1]
        self.eat()
        return Number(val)

    def parse_expr(self):
        left = self.parse_term()

        while self.current()[0] in ("PLUS", "MINUS"):
            op = self.current()[0]
            self.eat()
            right = self.parse_term()
            left = BinOp(left, op, right)

        return left

    def parse_term(self):
        token = self.current()

        if token[0] == "INT":
            return self.parse_number()

        if token[0] == "IDENT":
            name = token[1]
            self.eat()

            if self.current()[0] == "LPAREN":
                self.eat()
                arg = self.parse_expr()
                self.eat()
                return Call(name, arg)

            return Var(name)

        if token[0] == "STRING":
            val = token[1]
            self.eat()
            return String(val)

    def parse(self):
        statements = []

        while self.current()[0] != "EOF":
            token = self.current()

            if token[0] == "LET":
                self.eat()
                name = self.current()[1]
                self.eat()
                self.eat()
                expr = self.parse_expr()
                statements.append(Let(name, expr))

            elif token[0] == "PRINT":
                self.eat()
                expr = self.parse_expr()
                statements.append(Print(expr))

            else:
                self.eat()

        return statements