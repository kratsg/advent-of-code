import numpy as np
import re


def process_input(data):
    return np.array(data.split(","), dtype="int64")


def get_min(data, cost_func):
    mmax = data.max()
    guesses = np.arange(mmax)

    space = data[None, :]
    space = np.repeat(space, guesses.size, axis=0)
    space = np.abs(space - guesses[:, None])
    cost = cost_func(space)
    return int(guesses[cost.argmin()]), int(cost.min())


def min_cost_part1(space):
    return np.sum(space, axis=1)


def min_cost_part2(space):
    return np.sum(space * (space + 1) / 2, axis=1)


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input("""16,1,2,0,4,2,7,1,2,14""")

    assert get_min(test_vals, min_cost_part1) == (2, 37)

    puz = Puzzle(2021, 7)

    data = process_input(puz.input_data)

    puz.answer_a = get_min(data, min_cost_part1)[1]
    print(f"Part 1: {puz.answer_a}")

    assert get_min(test_vals, min_cost_part2) == (5, 168)

    puz.answer_b = get_min(data, min_cost_part2)[1]
    print(f"Part 2: {puz.answer_b}")
