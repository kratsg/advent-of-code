import numpy as np
from io import StringIO


def process_input(data):
    return np.genfromtxt(StringIO(data), dtype="int64", delimiter=1)


def event(grid):
    grid += 1
    flashed_mask = grid > 9
    grid[flashed_mask] = 0
    flashed_idx = set(map(tuple, np.argwhere(flashed_mask)))
    queue = list(flashed_idx)
    while queue:
        x, y = queue.pop(0)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                # skip out of bound points
                if (
                    x + i < 0
                    or y + j < 0
                    or x + i >= grid.shape[0]
                    or y + j >= grid.shape[1]
                ):
                    continue
                neighbor = (x + i, y + j)
                # don't increment points that flashed or will flash
                if neighbor in flashed_idx:
                    continue
                grid[neighbor] += 1
                if grid[neighbor] > 9:
                    flashed_idx.add(neighbor)
                    queue.append(neighbor)
                    grid[neighbor] = 0
    return grid, len(flashed_idx)


def part1(data):
    grid = np.array(data, copy=True)
    total_flashes = 0
    for _ in range(100):
        total_flashes += event(grid)[1]
    return total_flashes


def part2(data):
    grid = np.array(data, copy=True)
    i = 0
    while not np.all(grid == 0):
        event(grid)
        i += 1
    return i


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
    )

    puz = Puzzle(2021, 11)

    data = process_input(puz.input_data)

    assert part1(test_vals) == 1656

    puz.answer_a = part1(data)
    print(f"Part 1: {puz.answer_a}")

    assert part2(test_vals) == 195

    puz.answer_b = part2(data)
    print(f"Part 2: {puz.answer_b}")
