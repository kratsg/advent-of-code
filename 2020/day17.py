import numpy as np
from io import StringIO


def process_input(data):
    return np.genfromtxt(StringIO(data), dtype="|U1", delimiter=1, comments="S")


def build_grid(data, part2=False):
    if not part2:
        grid = np.chararray((*data.shape, 3), unicode=True)
        grid[:] = "."
        grid[..., 1] = data

    if part2:
        grid = np.chararray((*data.shape, 3, 3), unicode=True)
        grid[:] = "."
        grid[..., 1, 1] = data

    return grid


def pad_grid(data):
    return np.pad(data, 1, mode="constant", constant_values=".")


def count_active(data):
    return np.sum(data == "#")


def get_slice(index, size):
    return slice(max(0, index - 1), min(size - 1, index + 2))


def tick(data, part2=False):
    data = pad_grid(data)
    # create inactive new state
    new_state = np.copy(data)
    # get centers
    shape = data.shape
    if not part2:
        shape = (*shape, 1)

    x, y, z, w = shape

    for l in range(w):
        for k in range(z):
            for i in range(x):
                for j in range(y):
                    # what's up at the center
                    center = (i, j, k)
                    slices = (get_slice(i, x), get_slice(j, y), get_slice(k, z))

                    if part2:
                        center = (*center, l)
                        slices = (*slices, get_slice(l, w))

                    is_active = data[center] == "#"
                    neighbors = data[slices]
                    # skip counting the center
                    num_active = count_active(neighbors) - int(is_active)
                    if is_active:
                        if num_active not in [2, 3]:
                            new_state[center] = "."
                    else:
                        if num_active == 3:
                            new_state[center] = "#"

    return new_state


def execute(data, num_ticks=6, part2=False):
    for i in range(num_ticks):
        data = tick(data, part2=part2)
    return data


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """.#.
..#
###"""
    )
    test_grid = build_grid(test_vals)
    test_final_grid = execute(test_grid)
    assert count_active(test_final_grid) == 112

    puz = Puzzle(2020, 17)

    data = process_input(puz.input_data)
    grid = build_grid(data)
    final_grid = execute(grid)
    puz.answer_a = count_active(final_grid)
    print(f"Part 1: {puz.answer_a}")

    test_grid = build_grid(test_vals, part2=True)
    test_final_grid = execute(test_grid, part2=True)
    assert count_active(test_final_grid) == 848

    grid = build_grid(data, part2=True)
    final_grid = execute(grid, part2=True)

    puz.answer_b = count_active(final_grid)
    print(f"Part 2: {puz.answer_b}")
