import numpy as np
from io import StringIO


def process_input(data):
    myfile = StringIO(data.replace(".", "0").replace("#", "1"))
    return np.genfromtxt(myfile, delimiter=1, dtype=int)


def generate_steps(mapdata, start=None, step=None):
    indices = []
    start = start if start is not None else np.array([0, 0])
    step = step if step is not None else np.array([1, 3])  # right 3, down 1
    position = start
    # while less than total height of map
    while position[0] < mapdata.shape[0]:
        position[1] = position[1] % mapdata.shape[1]
        indices.append(tuple(position))
        position += step
    # skip first step
    return indices[1:]


def get_encounters(mapdata, start=None, step=None):
    steps = generate_steps(mapdata, start=start, step=step)
    indices = tuple(zip(*steps))
    return mapdata[indices]


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
    )
    encounters = get_encounters(test_vals, step=np.array([1, 3]))
    assert len(encounters) == 10
    assert encounters.tolist() == [0, 1, 0, 1, 1, 0, 1, 1, 1, 1]
    assert np.sum(encounters) == 7

    puz = Puzzle(2020, 3)

    data = process_input(puz.input_data)
    encounters = get_encounters(data, step=np.array([1, 3]))

    puz.answer_a = np.sum(encounters)
    print(f"Part 1: {puz.answer_a}")

    test_encounters_1_1 = get_encounters(test_vals, step=np.array([1, 1]))
    test_encounters_3_1 = get_encounters(test_vals, step=np.array([1, 3]))
    test_encounters_5_1 = get_encounters(test_vals, step=np.array([1, 5]))
    test_encounters_7_1 = get_encounters(test_vals, step=np.array([1, 7]))
    test_encounters_1_2 = get_encounters(test_vals, step=np.array([2, 1]))
    assert np.sum(test_encounters_1_1) == 2
    assert np.sum(test_encounters_3_1) == 7
    assert np.sum(test_encounters_5_1) == 3
    assert np.sum(test_encounters_7_1) == 4
    assert np.sum(test_encounters_1_2) == 2
    assert (
        np.sum(test_encounters_1_1)
        * np.sum(test_encounters_3_1)
        * np.sum(test_encounters_5_1)
        * np.sum(test_encounters_7_1)
        * np.sum(test_encounters_1_2)
        == 336
    )

    encounters_1_1 = get_encounters(data, step=np.array([1, 1]))
    encounters_3_1 = get_encounters(data, step=np.array([1, 3]))
    encounters_5_1 = get_encounters(data, step=np.array([1, 5]))
    encounters_7_1 = get_encounters(data, step=np.array([1, 7]))
    encounters_1_2 = get_encounters(data, step=np.array([2, 1]))

    puz.answer_b = (
        np.sum(encounters_1_1)
        * np.sum(encounters_3_1)
        * np.sum(encounters_5_1)
        * np.sum(encounters_7_1)
        * np.sum(encounters_1_2)
    )
    print(f"Part 2: {puz.answer_b}")
