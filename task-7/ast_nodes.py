class Number:
    def __init__(self, value):
        self.value = int(value)

class String:
    def __init__(self, value):
        self.value = value.strip('"')

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Print:
    def __init__(self, expr):
        self.expr = expr

class Let:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Var:
    def __init__(self, name):
        self.name = name

class Function:
    def __init__(self, name, param, body):
        self.name = name
        self.param = param
        self.body = body

class Call:
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg

class Return:
    def __init__(self, value):
        self.value = value