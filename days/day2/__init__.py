def parse_input(input_string: str) -> list[tuple[str, str]]:
    """Parses the input string into a list of tuples.

    >>> parse_input("11-22,95-115")
    [('11', '22'), ('95', '115')]
    """

    def line_split(line: str) -> tuple[str, str]:
        a, b = tuple(line.split("-"))
        return a, b

    return [line_split(line) for line in input_string.strip().split(",")]


def parse_input_file(file_path: str) -> list[tuple[str, str]]:
    """Reads the input file and parses its content."""

    with open(file_path, "r") as file:
        input_string = file.read()
    return parse_input(input_string)


def find_invalids_1(a: str, b: str) -> list[int]:
    """
    >>> find_invalids_1('122000', '124999')
    [122122, 123123, 124124]
    >>> find_invalids_1('1220000', '1240000')
    []
    """

    assert len(a) == len(b)
    if len(a) % 2 != 0:
        return []

    prefix_len = len(a) // 2
    start = int(a[:prefix_len])
    end = int(b[:prefix_len])

    invalids = []
    for prefix in range(start, end + 1):
        prefix_str = str(prefix)
        duplicate = int(prefix_str + prefix_str)
        if duplicate >= int(a) and duplicate <= int(b):
            invalids.append(duplicate)

    return invalids


def find_invalids_2(a: str, b: str) -> list[int]:
    """
    >>> find_invalids_2('1', '2')
    []
    >>> find_invalids_2('11', '22')
    [11, 22]
    >>> find_invalids_2('95', '99')
    [99]
    >>> find_invalids_2('100', '115')
    [111]
    >>> find_invalids_2('998', '999')
    [999]
    >>> find_invalids_2('1000', '1012')
    [1010]
    >>> find_invalids_2('1188511880', '1188511890')
    [1188511885]
    """

    assert len(a) == len(b)

    invalids = []
    for prefix_len in range(1, (len(a) // 2) + 1):
        if len(a) % prefix_len != 0:
            continue

        mult_count = len(a) // prefix_len

        start = int(a[:prefix_len])
        end = int(b[:prefix_len])

        for prefix in range(start, end + 1):
            prefix_str = str(prefix)
            duplicate = int(prefix_str * mult_count)
            if (
                duplicate >= int(a)
                and duplicate <= int(b)
                and duplicate not in invalids
            ):
                invalids.append(duplicate)

    return invalids


def even_digits(num: int) -> bool:
    """Checks if the number has an even number of digits.

    >>> even_digits(1234)
    True
    >>> even_digits(123)
    False
    """

    return len(str(num)) % 2 == 0


def subdivide(a: str, b: str) -> list[tuple[str, str]]:
    """Subdivides the range into smaller ranges based on prefix.

    >>> subdivide('95', '115')
    [('95', '99'), ('100', '115')]
    >>> subdivide('10', '10000')
    [('10', '99'), ('100', '999'), ('1000', '9999'), ('10000', '10000')]
    """

    start = int(a)
    end = int(b)

    start_digit_count = len(a)
    end_digit_count = len(b)

    ranges = []
    for digit_count in range(start_digit_count, end_digit_count + 1):
        if digit_count == start_digit_count:
            range_start = start
        else:
            range_start = 10 ** (digit_count - 1)

        if digit_count == end_digit_count:
            range_end = end
        else:
            range_end = (10**digit_count) - 1

        ranges.append((str(range_start), str(range_end)))

    return ranges


def solve_star1(items: list[tuple[str, str]]) -> int:
    """Solves star 1.

    >>> solve_star1([('11', '22'), ('95', '115')])
    132
    """

    sum_invalids = 0
    for a, b in items:
        ranges = subdivide(a, b)
        for sub_a, sub_b in ranges:
            sum_invalids += sum(find_invalids_1(sub_a, sub_b))
    return sum_invalids


def solve_star2(input_str: str) -> int:
    """Solves star 2.

    >>> solve_star2('11-22,95-115')
    243
    >>> solve_star2('11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124')
    4174379265
    """

    items = parse_input(input_str)

    sum_invalids = 0
    for a, b in items:
        ranges = subdivide(a, b)
        for sub_a, sub_b in ranges:
            sum_invalids += sum(find_invalids_2(sub_a, sub_b))
    return sum_invalids


def star1(input_str: str) -> None:
    items = parse_input(input_str)
    result = solve_star1(items)
    print(result)


def star2(input_str: str) -> None:
    result = solve_star2(input_str)
    print(result)
