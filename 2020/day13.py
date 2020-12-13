def process_input(data):
    timestamp, busses = data.split("\n")
    timestamp = int(timestamp)
    busses = list(
        map(lambda x: float("inf") if x == "x" else int(x), busses.split(","))
    )
    return (timestamp, busses)


def find_earliest_bus(start_timestamp, busses):
    valid_busses = [bus for bus in busses if bus < float("inf")]
    timestamp = start_timestamp
    while True:
        for bus in busses:
            if timestamp % bus == 0:
                return (timestamp, bus)
        timestamp += 1


import itertools


def find_smallest_bus_timestamp(busses):
    busses = [(i, bus) for i, bus in enumerate(busses) if bus < float("inf")]
    start, steps = busses[0]
    """
    a way to solve this is by starting with each bus and counting up in increments of that bus number.

    we start with first bus and it's offset and count up. If the second bus does not fit in this, step up, then we continue.
    otherwise, we alter the steps to include the next bus as well (since we found what the next valid timestamp must be).
    """
    for offset, bus in busses[1:]:
        for timestamp in itertools.count(start, steps):
            # did we find the start of the next arithmetic sequence
            if (timestamp + offset) % bus:
                continue
            # hit a situation where we can include the next bus in current arithmetic sequence
            start = timestamp
            steps *= bus
            break
    return timestamp


# note: from https://rosettacode.org/wiki/Chinese_remainder_theorem
import operator
import functools


def chinese_remainder_theorem(numbers, remainders):
    sum = 0
    big_N = functools.reduce(operator.mul, numbers, 1)
    for n_i, a_i in zip(numbers, remainders):
        p = big_N // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % big_N


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def find_sequential_bus_timestamp(busses):
    """
    Recall for chinese remainder theorem that

    N   ≡ 0 (mod x0)
    N+1 ≡ 0 (mod x1)
    N+2 ≡ 0 (mod x2)

    is equivalent to

    N ≡  0 (mod x0)
    N ≡ -1 (mod x1)
    N ≡ -2 (mod x2)

    so generalizing this, we need the same "N". Math it out so that

    N ≡ 0 mod x0
    N ≡ (x1 - 1) mod x1
    ...
    N ≡ (xi - i) mod xi
    """
    modulos = list(
        zip(
            *[
                (bus, (bus - i) % bus)
                for i, bus in enumerate(busses)
                if bus < float("inf")
            ]
        )
    )
    return chinese_remainder_theorem(*modulos)


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """939
7,13,x,x,59,x,31,19"""
    )
    test_timestamp, test_bus = find_earliest_bus(*test_vals)
    assert test_timestamp == 944
    assert test_bus == 59
    assert (test_timestamp - test_vals[0]) * test_bus == 295

    puz = Puzzle(2020, 13)

    data = process_input(puz.input_data)
    timestamp, bus = find_earliest_bus(*data)

    puz.answer_a = (timestamp - data[0]) * bus
    print(f"Part 1: {puz.answer_a}")

    assert find_smallest_bus_timestamp([17, float("inf"), 13, 19]) == 3417
    assert find_smallest_bus_timestamp([67, 7, 59, 61]) == 754018
    assert find_smallest_bus_timestamp([67, float("inf"), 7, 59, 61]) == 779210
    assert find_smallest_bus_timestamp([67, 7, float("inf"), 59, 61]) == 1261476
    assert find_smallest_bus_timestamp([1789, 37, 47, 1889]) == 1202161486

    assert find_sequential_bus_timestamp([17, float("inf"), 13, 19]) == 3417
    assert find_sequential_bus_timestamp([67, 7, 59, 61]) == 754018
    assert find_sequential_bus_timestamp([67, float("inf"), 7, 59, 61]) == 779210
    assert find_sequential_bus_timestamp([67, 7, float("inf"), 59, 61]) == 1261476
    assert find_sequential_bus_timestamp([1789, 37, 47, 1889]) == 1202161486

    puz.answer_b = find_smallest_bus_timestamp(data[1])
    print(f"Part 2: {puz.answer_b}")
