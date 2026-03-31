from ast_nodes import *

class Interpreter:
    def __init__(self):
        self.env = {}

    def eval(self, node):
        if isinstance(node, Number):
            return node.value

        if isinstance(node, String):
            return node.value

        if isinstance(node, Var):
            return self.env[node.name]

        if isinstance(node, BinOp):
            left = self.eval(node.left)
            right = self.eval(node.right)

            if node.op == "PLUS":
                return left + right
            if node.op == "MINUS":
                return left - right

        if isinstance(node, Let):
            self.env[node.name] = self.eval(node.value)

        if isinstance(node, Print):
            print(self.eval(node.expr))