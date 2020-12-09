import itertools


def process_input(data):
    results = list(map(int, data.split("\n")))
    return results


def find_broken_chunk(data, preamble_size=25):
    for i in range(len(data) - preamble_size):
        combos = list(map(sum, itertools.combinations(data[i : i + preamble_size], 2)))
        if data[i + preamble_size] not in combos:
            return i + preamble_size
    return None


def find_contiguous_sum(data, number):
    for i in range(len(data)):
        for j in range(len(data) - i - 1):
            total = sum(data[i : i + j])
            if total == int(number):
                return data[i : i + j]
            if total > int(number):
                break


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""
    )
    bad_index = find_broken_chunk(test_vals, preamble_size=5)
    assert bad_index is not None
    assert test_vals[bad_index] == 127

    puz = Puzzle(2020, 9)

    data = process_input(puz.input_data)
    bad_index = find_broken_chunk(data)

    puz.answer_a = data[bad_index]
    print(f"Part 1: {puz.answer_a}")

    numbers = find_contiguous_sum(test_vals, 127)
    assert numbers == [15, 25, 47, 40]
    assert max(numbers) + min(numbers) == 62

    numbers = find_contiguous_sum(data, puz.answer_a)
    puz.answer_b = max(numbers) + min(numbers)
    print(f"Part 2: {puz.answer_b}")
