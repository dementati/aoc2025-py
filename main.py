import argparse


def main():
    parser = argparse.ArgumentParser(description="Run Advent of Code 2025 solutions.")
    parser.add_argument("day", type=int, help="Day of the challenge (1-25)")
    parser.add_argument(
        "star", type=int, choices=[1, 2], help="Star of the challenge (1 or 2)"
    )
    args = parser.parse_args()

    day = args.day
    star = args.star

    module_name = f"days.day{day}.star{star}"
    try:
        module = __import__(module_name, fromlist=[""])
        if hasattr(module, "run"):
            module.run()
        else:
            print(f"The module {module_name} does not have a run() function.")
    except ImportError:
        print(f"Module {module_name} not found.")


if __name__ == "__main__":
    main()
