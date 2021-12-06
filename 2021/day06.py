import numpy as np
import re


def process_input(data):
    fish = np.array(data.split(","), dtype="int64")
    return {i: np.sum(fish == i) for i in range(9)}


def timer(fish):
    fish[8], fish[7], fish[6], fish[5], fish[4], fish[3], fish[2], fish[1], fish[0] = (
        fish[0],
        fish[8],
        fish[7] + fish[0],
        fish[6],
        fish[5],
        fish[4],
        fish[3],
        fish[2],
        fish[1],
    )


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input("""3,4,3,1,2""")

    for _ in range(80):
        timer(test_vals)

    assert sum(test_vals.values()) == 5934

    puz = Puzzle(2021, 6)

    data = process_input(puz.input_data)

    for _ in range(80):
        timer(data)

    puz.answer_a = sum(data.values())
    print(f"Part 1: {puz.answer_a}")

    for _ in range(256 - 80):
        timer(data)

    puz.answer_b = sum(data.values())
    print(f"Part 2: {puz.answer_b}")
