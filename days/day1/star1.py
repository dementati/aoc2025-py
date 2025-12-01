from days.day1 import parse_input_file, solve_star1


def run():
    instructions = parse_input_file("days/day1/input.txt")
    print(solve_star1(instructions))
