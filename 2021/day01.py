def process_input(data):
    return list(map(int, data.split()))


def window(sequence, size=2):
    it = iter(sequence)
    result = [next(it) for _ in range(size)]
    if len(result) == size:
        yield result
    for element in it:
        result = result[1:] + [element]
        yield result


def part1(sequence):
    return sum(map(lambda x: x[-1] > x[0], window(sequence, size=2)))


def part2(sequence):
    return sum(map(lambda x: x[-1] > x[0], window(sequence, size=6)))


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """199
200
208
210
200
207
240
269
260
263"""
    )

    assert part1(test_vals) == 7

    puz = Puzzle(2021, 1)

    numbers = list(map(int, puz.input_data.split()))

    puz.answer_a = part1(numbers)
    print(f"Part 1: {puz.answer_a}")

    assert part2(test_vals) == 5

    puz.answer_b = part2(numbers)
    print(f"Part 2: {puz.answer_b}")
