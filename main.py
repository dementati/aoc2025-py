# ...existing code...
import argparse
import importlib
import time


def main():
    parser = argparse.ArgumentParser(description="Run Advent of Code 2025 solutions.")
    parser.add_argument("day", type=int, help="Day of the challenge (1-25)")
    parser.add_argument(
        "star", type=int, choices=[1, 2], help="Star of the challenge (1 or 2)"
    )
    parser.add_argument("-f", "--func", type=str, help="Optional function name to run")
    args = parser.parse_args()

    day = args.day
    star = args.star

    module_name = f"days.day{day}"
    func_name = f"star{star}" if not args.func else args.func
    print(f"Running {module_name}.{func_name}()...")
    try:
        module = importlib.import_module(module_name)
        func = getattr(module, func_name, None)

        with open(f"days/day{day}/input.txt") as file:
            input_str = file.read()

        if func is None:
            print(
                f"The module {module_name} does not define a function named {func_name}()."
            )
            return
        if not callable(func):
            print(f"{module_name}.{func_name} exists but is not callable.")
            return

        start = time.perf_counter_ns()
        result = func(input_str)
        print(f"{(time.perf_counter_ns() - start) / 1_000_000_000} s")
        print(f"{(time.perf_counter_ns() - start) / 1_000_000} ms")
        print(f"{(time.perf_counter_ns() - start) / 1_000} µs")
        print(f"Result: {result}")
    except ModuleNotFoundError:
        print(f"Module {module_name} not found.")
    except Exception as e:
        print(f"Error running {module_name}.{func_name}(): {e}")


if __name__ == "__main__":
    main()
