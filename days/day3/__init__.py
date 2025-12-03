def joltage(battery: str, size: int) -> int:
    """Calculates the joltage of the battery string.

    >>> joltage('811111111111119', 2)
    89
    >>> joltage('987654321111111', 2)
    98
    >>> joltage('234234234234278', 2)
    78
    >>> joltage('818181911112111', 2)
    92
    >>> joltage('987654321111111', 12)
    987654321111
    >>> joltage('811111111111119', 12)
    811111111119
    >>> joltage('111111111111119', 2)
    19
    """

    idx = 0
    value = ""
    for i in range(size):
        start = idx
        end = i + -size + 1
        if end == 0:
            end = None

        mx = max(battery[start:end])
        idx = battery.index(mx, start, end) + 1
        value += mx

    return int(value)


def joltage_stack(battery: str, size: int) -> int:
    """Calculates the joltage of the battery string.

    >>> joltage_stack('811111111111119', 2)
    89
    >>> joltage_stack('987654321111111', 2)
    98
    >>> joltage_stack('234234234234278', 2)
    78
    >>> joltage_stack('818181911112111', 2)
    92
    >>> joltage_stack('987654321111111', 12)
    987654321111
    >>> joltage_stack('811111111111119', 12)
    811111111119
    """

    n = len(battery)
    stack = []
    for i, c in enumerate(battery):
        remaining = n - i

        if not stack:
            stack.append(c)
            continue

        while c > stack[-1] and len(stack) + remaining > size:
            stack.pop()
            if not stack:
                break

        if len(stack) < size:
            stack.append(c)

    return int("".join(stack))


def star1(input_str: str) -> str:
    """
    >>> star1('811111111111119\\n987654321111111\\n234234234234278\\n818181911112111')
    '357'
    """
    batteries = input_str.strip().split("\n")
    total_joltage = sum(joltage(battery, 2) for battery in batteries)
    return str(total_joltage)


def star2(input_str: str) -> str:
    """
    >>> star2('811111111111119\\n987654321111111\\n234234234234278\\n818181911112111')
    '3121910778619'
    """
    batteries = input_str.strip().split("\n")
    total_joltage = sum(joltage(battery, 12) for battery in batteries)
    return str(total_joltage)


def star2_stack(input_str: str) -> str:
    """
    >>> star2('811111111111119\\n987654321111111\\n234234234234278\\n818181911112111')
    '3121910778619'
    """
    batteries = input_str.strip().split("\n")
    total_joltage = sum(joltage_stack(battery, 12) for battery in batteries)
    return str(total_joltage)
