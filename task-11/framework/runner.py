import os
import importlib.util
from multiprocessing import Pool
from framework.decorators import TESTS
from framework.core import run_test

def discover_tests(test_dir):
    for file in os.listdir(test_dir):
        if file.startswith("test_") and file.endswith(".py"):
            path = os.path.join(test_dir, file)

            spec = importlib.util.spec_from_file_location(file, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

def execute_tests(parallel=1):
    print("\n=== Test Discovery ===")
    print(f"Found {len(TESTS)} tests\n")

    # ⚠️ Disable multiprocessing due to pickling issues on Windows
    results = [run_test(t) for t in TESTS]

    return results