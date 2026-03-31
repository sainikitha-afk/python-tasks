import sys
import os

# Ensure current directory is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from framework.runner import discover_tests, execute_tests


def main():
    test_dir = "tests"
    parallel = 1

    # Parse CLI arguments
    if "--parallel" in sys.argv:
        idx = sys.argv.index("--parallel")
        parallel = int(sys.argv[idx + 1])

    # Discover tests
    discover_tests(test_dir)

    # Execute tests
    results = execute_tests(parallel)

    passed = failed = skipped = 0

    print("\n=== Execution ===")

    for status, name, msg, duration in results:
        print(f"{status:<5} {name:<40} [{duration}s]")

        if status == "PASS":
            passed += 1
        elif status == "FAIL":
            failed += 1
            print(f"      AssertionError: {msg}")
        elif status == "SKIP":
            skipped += 1
            print(f"      skipped: {msg}")

    print("\n=== Summary ===")
    print(f"{len(results)} tests | {passed} passed | {failed} failed | {skipped} skipped")


if __name__ == "__main__":
    main()