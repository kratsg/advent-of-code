import numpy as np


def process_input(data):
    return np.array(list("".join(data.splitlines())), dtype="int64").reshape(
        -1, len(data.splitlines()[0])
    )


def find_lowest_points(data):
    mask = None
    for shift in [-1, 1]:
        for axis in [0, 1]:
            new_mask = (np.roll(data, shift, axis=axis) - data) > 0
            mask = new_mask & mask if mask is not None else new_mask

    return mask


def calculate_risk(points):
    return int((points + 1).sum())


def identify_basins(data, point, basin_set):
    basin_set.add(tuple(point))
    x, y = point
    for i, j in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if i < 0:
            continue
        if j < 0:
            continue
        if i >= data.shape[0]:
            continue
        if j >= data.shape[1]:
            continue
        if (i, j) in basin_set:
            continue
        compare = data[i, j]
        if compare == 9:
            continue
        identify_basins(data, (i, j), basin_set)
    return basin_set


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """2199943210
3987894921
9856789892
8767896789
9899965678"""
    )

    test_padded = np.pad(test_vals, 1, mode="maximum")
    test_where_lowest = find_lowest_points(test_padded)
    test_lowest_points = test_padded[test_where_lowest]
    assert calculate_risk(test_lowest_points) == 15

    puz = Puzzle(2021, 9)

    data = process_input(puz.input_data)
    padded = np.pad(data, 1, mode="maximum")
    where_lowest = find_lowest_points(padded)
    lowest_points = padded[where_lowest]

    puz.answer_a = calculate_risk(lowest_points)
    print(f"Part 1: {puz.answer_a}")

    test_basins = []
    for lowest_point in np.argwhere(test_where_lowest):
        test_basins.append(len(identify_basins(test_padded, lowest_point, set())))

    assert test_basins == [3, 9, 14, 9]

    puz.answer_b = int(
        np.prod(
            sorted(
                len(identify_basins(padded, lowest_point, set()))
                for lowest_point in np.argwhere(where_lowest)
            )[-3:]
        )
    )
    print(f"Part 2: {puz.answer_b}")
