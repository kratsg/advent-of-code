import numpy as np
import re

pattern = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


def process_input(data):
    return np.array(pattern.findall(data), dtype="int64")


def build_grid(coordinates, include_diag=False):
    xmax = coordinates[:, [0, 2]].max()
    ymax = coordinates[:, [1, 3]].max()
    grid = np.full((xmax + 1, ymax + 1), 0)

    for x1, y1, x2, y2 in coordinates:
        # skip anything but horizontal/vertical
        if x1 != x2 and y1 != y2 and not include_diag:
            continue
        if bool(x1 == x2) ^ bool(y1 == y2):
            # make sure we sort them
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            grid[y1 : y2 + 1, x1 : x2 + 1] += 1
        else:
            # diagonal
            xpoints = np.arange(x1, x2 + np.sign(x2 - x1), np.sign(x2 - x1))
            ypoints = np.arange(y1, y2 + np.sign(y2 - y1), np.sign(y2 - y1))
            grid[ypoints, xpoints] += 1
    return grid


def count_overlaps(grid):
    return np.sum(grid >= 2)


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
    )

    grid = build_grid(test_vals)

    assert grid.tolist() == [
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 2, 1, 1, 1, 2, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 2, 2, 1, 1, 1, 0, 0, 0, 0],
    ]

    assert count_overlaps(grid) == 5

    puz = Puzzle(2021, 5)

    data = process_input(puz.input_data)
    grid = build_grid(data)

    puz.answer_a = count_overlaps(grid)
    print(f"Part 1: {puz.answer_a}")

    grid = build_grid(test_vals, True)
    assert grid.tolist() == [
        [1, 0, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 1, 0, 0, 0, 2, 0, 0],
        [0, 0, 2, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 2, 0, 2, 0, 0],
        [0, 1, 1, 2, 3, 1, 3, 2, 1, 1],
        [0, 0, 0, 1, 0, 2, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [2, 2, 2, 1, 1, 1, 0, 0, 0, 0],
    ]
    assert count_overlaps(grid) == 12

    grid = build_grid(data, True)
    puz.answer_b = count_overlaps(grid)
    print(f"Part 2: {puz.answer_b}")
