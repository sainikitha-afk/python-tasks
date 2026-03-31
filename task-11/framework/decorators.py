import functools

TESTS = []
FIXTURES = {}

def test(func):
    TESTS.append(func)
    return func

def skip(reason=""):
    def decorator(func):
        func._skip = reason
        return func
    return decorator

def parametrize(arg_name, values):
    def decorator(func):
        func._params = [(arg_name, v) for v in values]
        return func
    return decorator

def fixture(scope="function"):
    def decorator(func):
        FIXTURES[func.__name__] = func
        return func
    return decorator