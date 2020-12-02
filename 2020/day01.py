import itertools
import math


def process_input(data):
    return list(map(int, data.split()))


def find_set(items, n=2, total=2020):
    for combination in itertools.combinations(items, n):
        if sum(combination) == total:
            return combination


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """
1721
979
366
299
675
1456"""
    )

    assert find_set(test_vals, 2) == (1721, 299)
    assert math.prod(find_set(test_vals, 2)) == 514579

    assert find_set(test_vals, 3) == (979, 366, 675)
    assert math.prod(find_set(test_vals, 3)) == 241861950
    puz = Puzzle(2020, 1)

    numbers = list(map(int, puz.input_data.split()))

    puz.answer_a = math.prod(find_set(numbers, 2))
    print(f"Part 1: {puz.answer_a}")

    puz.answer_b = math.prod(find_set(numbers, 3))
    print(f"Part 2: {puz.answer_b}")
