from days.day1 import parse_input_file, solve_star2


def run():
    instructions = parse_input_file("days/day1/input.txt")
    print(solve_star2(instructions))
