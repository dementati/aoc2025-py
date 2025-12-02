# ...existing code...
import argparse
import importlib


def main():
    parser = argparse.ArgumentParser(description="Run Advent of Code 2025 solutions.")
    parser.add_argument("day", type=int, help="Day of the challenge (1-25)")
    parser.add_argument(
        "star", type=int, choices=[1, 2], help="Star of the challenge (1 or 2)"
    )
    args = parser.parse_args()

    day = args.day
    star = args.star

    module_name = f"days.day{day}"
    func_name = f"star{star}"
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
        func(input_str)
    except ModuleNotFoundError:
        print(f"Module {module_name} not found.")
    except Exception as e:
        print(f"Error running {module_name}.{func_name}(): {e}")


if __name__ == "__main__":
    main()
