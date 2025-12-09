import argparse
import doctest
import importlib
import sys
import timeit
from typing import Callable, cast


def run_function(
    day: int,
    func_name: str,
    profile_performance: bool,
    use_example: bool,
    count: int | None = None,
) -> None:
    module_name = f"days.day{day}"
    print(
        f"{'Profiling' if profile_performance else 'Running'} {module_name}.{func_name}()..."
    )

    try:
        module = importlib.import_module(module_name)
        func = cast(Callable[[str], str], getattr(module, func_name, None))

        file_path = "examples/1.txt" if use_example else "input.txt"

        with open(f"days/day{day}/{file_path}") as file:
            input_str = file.read()

        if func is None:
            print(
                f"The module {module_name} does not define a function named {func_name}()."
            )
            return
        if not callable(func):
            print(f"{module_name}.{func_name} exists but is not callable.")
            return

        if profile_performance:

            def benchmark():
                func(input_str)

            timer = timeit.Timer(benchmark)

            def profile_once():
                number, total = timer.autorange()
                per_call = total / number
                return per_call, total, number

            if count:
                results = []

                for _ in range(count):
                    per_call, _, _ = profile_once()
                    results.append(per_call)

                mean, stddev = (
                    sum(results) / count,
                    (sum((x - sum(results) / count) ** 2 for x in results) / count)
                    ** 0.5,
                )
                minimum = min(results)

                print(f"{mean:.6f} ± {stddev:.6f} seconds over {count} runs.")
                print(f"Min: {minimum:.6f} seconds.")
            else:
                per_call, total, number = profile_once()

                print(f"Executed {number} times in {total:.6f} seconds.")
                print(f"{per_call:.6f} s")
                print(f"{per_call * 1000:.6f} ms")
                print(f"{per_call * 1_000_000:.6f} µs")
            return

        result = func(input_str)
        print(f"Result: {result}")
    except ModuleNotFoundError:
        print(f"Module {module_name} not found.")
    except Exception as e:
        print(f"Error running {module_name}.{func_name}(): {e}")


def main():
    parser = argparse.ArgumentParser(description="Run Advent of Code 2025 solutions.")
    parser.add_argument("day", type=int, help="Day of the challenge (1-25)")
    parser.add_argument(
        "-s",
        "--star",
        type=int,
        choices=[1, 2],
        help="Optional star of the challenge (1 or 2) to run",
    )
    parser.add_argument("-f", "--func", type=str, help="Optional function name to run")
    parser.add_argument(
        "-e", "--example", action="store_true", help="Use example input"
    )
    parser.add_argument("-p", "--perf", action="store_true", help="Profile performance")
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        help="Number of times to run for performance profiling",
    )
    parser.add_argument(
        "-t", "--test", action="store_true", help="Run tests (doctests)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output for tests"
    )
    args = parser.parse_args()

    day = args.day

    if args.test:
        module_name = f"days.day{day}"
        print(f"Running tests for {module_name}...")
        try:
            module = importlib.import_module(module_name)

            result = doctest.testmod(module, verbose=args.verbose)
            if result.failed:
                print(f"Tests failed: {result.failed} failures.")
                sys.exit(1)
            else:
                print("All tests passed.")
        except ModuleNotFoundError:
            print(f"Module {module_name} not found.")

    if args.func:
        func_names = [args.func]
    elif args.star:
        func_names = [f"star{args.star}"]
    else:
        func_names = [f"star1", f"star2"]

    for func_name in func_names:
        run_function(day, func_name, args.perf, args.example, args.count)


if __name__ == "__main__":
    main()
