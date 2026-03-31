import traceback
import time

def run_test(func, verbose=False):
    start = time.time()

    if hasattr(func, "_skip"):
        return ("SKIP", func.__name__, func._skip, 0)

    try:
        func()
        duration = round(time.time() - start, 3)
        return ("PASS", func.__name__, "", duration)

    except AssertionError as e:
        duration = round(time.time() - start, 3)
        return ("FAIL", func.__name__, str(e), duration)

    except Exception as e:
        duration = round(time.time() - start, 3)
        return ("ERROR", func.__name__, str(e), duration)