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


def tick(data, part2=False):
    data = pad_grid(data)
    # create inactive new state
    new_state = np.copy(data)
    # get centers
    x, y, z = data.shape
    xc, yc, zc = x // 2, y // 2, z // 2
    for k in range(z):
        for i in range(x):
            for j in range(y):
                # what's up at the center
                center = (i, j, k)
                is_active = data[center] == "#"
                ilo = max(0, i - 1)
                jlo = max(0, j - 1)
                klo = max(0, k - 1)
                ihi = min(x - 1, i + 2)
                jhi = min(y - 1, j + 2)
                khi = min(z - 1, k + 2)
                neighbors = data[ilo:ihi, jlo:jhi, klo:khi]
                # skip counting the center
                num_active = count_active(neighbors) - int(is_active)
                if is_active:
                    if num_active not in [2, 3]:
                        new_state[center] = "."
                else:
                    if num_active == 3:
                        new_state[center] = "#"

    return new_state


def tick_part2(data):
    data = pad_grid(data)
    # create inactive new state
    new_state = np.copy(data)
    # get centers
    x, y, z, w = data.shape
    xc, yc, zc, wc = x // 2, y // 2, z // 2, w // 2
    for l in range(w):
        for k in range(z):
            for i in range(x):
                for j in range(y):
                    # what's up at the center
                    center = (i, j, k, l)
                    is_active = data[center] == "#"
                    ilo = max(0, i - 1)
                    jlo = max(0, j - 1)
                    klo = max(0, k - 1)
                    llo = max(0, l - 1)
                    ihi = min(x - 1, i + 2)
                    jhi = min(y - 1, j + 2)
                    khi = min(z - 1, k + 2)
                    lhi = min(w - 1, l + 2)
                    neighbors = data[ilo:ihi, jlo:jhi, klo:khi, llo:lhi]
                    # skip counting the center
                    num_active = count_active(neighbors) - int(is_active)
                    if is_active:
                        if num_active not in [2, 3]:
                            new_state[center] = "."
                    else:
                        if num_active == 3:
                            new_state[center] = "#"

    return new_state


def print_grid(data):
    x, y, z = data.shape
    xc, yc, zc = x // 2, y // 2, z // 2
    for i in range(z):
        subset = grid[:, :, i]
        if np.sum(subset == "#") == 0:
            continue
        print(f"z={i-zc}")
        print("\n".join("".join(x) for x in grid[:, :, i] if "#" in x))


def execute(data, num_ticks=6, part2=False):
    for i in range(6):
        if part2:
            data = tick_part2(data)
        else:
            data = tick(data)
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
