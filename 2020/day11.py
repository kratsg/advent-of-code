import numpy as np


def sliding_window(data, window_size, step_size):
    for i in range(0, data.shape[0] - window_size + 1):
        for j in range(0, data.shape[1] - window_size + 1):
            yield data[i : i + window_size, j : j + window_size].reshape(
                (-1, window_size)
            )


def process_input(data):
    central = np.asarray(
        list(map(tuple, data.replace("L", "1").replace(".", "0").split())), dtype="int"
    )
    result = np.full((central.shape[0] + 2, central.shape[1] + 2), 0)
    result[1:-1, 1:-1] = central
    return result


def count_occupied(data):
    return np.sum(np.array(data) == 2)


def any_occupied(data):
    return np.any(data == 2)


def tick_part1(data):
    result = []
    for window in sliding_window(data, 3, 1):
        center = window[1, 1]
        occupied = count_occupied(window)
        if center == 1 and occupied == 0:
            new_center = 2
        elif center == 2 and occupied >= 5:
            new_center = 1
        else:
            new_center = center

        result.append(new_center)
    result = np.array(result).reshape((data.shape[0] - 2, data.shape[1] - 2))
    data[1:-1, 1:-1] = result


def closest_seat(data):
    try:
        return next(i for i in data if i in [1, 2])
    except StopIteration:
        return 0


def tick_part2(data):
    datasub = data[1:-1, 1:-1]
    result = []
    for i in range(datasub.shape[0]):
        for j in range(datasub.shape[1]):
            center = datasub[i, j]
            datasub[i, j] = 99

            row = datasub[i, :]
            col = datasub[:, j]
            major = np.diagonal(datasub, offset=(j - i))
            minor = np.diagonal(
                np.rot90(datasub), offset=-datasub.shape[1] + (j + i) + 1
            )

            row_index = row.tolist().index(99)
            col_index = col.tolist().index(99)
            major_index = major.tolist().index(99)
            minor_index = minor.tolist().index(99)

            l = row[:row_index][::-1]
            r = row[row_index:]
            u = col[:col_index][::-1]
            d = col[col_index:]

            ul = major[:major_index][::-1]
            ur = minor[:minor_index][::-1]
            br = major[major_index:]
            bl = minor[minor_index:]

            seats = [
                closest_seat(l),
                closest_seat(r),
                closest_seat(u),
                closest_seat(d),
                closest_seat(ul),
                closest_seat(ur),
                closest_seat(br),
                closest_seat(bl),
            ]

            occupied = count_occupied(seats)
            if center == 1 and occupied == 0:
                new_center = 2
            elif center == 2 and occupied >= 5:
                new_center = 1
            else:
                new_center = center

            datasub[i, j] = center
            result.append(new_center)
    result = np.array(result).reshape((data.shape[0] - 2, data.shape[1] - 2))
    data[1:-1, 1:-1] = result


def process(indata, tick=tick_part1):
    data = np.array(indata, copy=True)
    prev_occupied = count_occupied(data)
    while True:
        tick(data)
        occupied = count_occupied(data)
        if occupied == prev_occupied:
            return occupied
        prev_occupied = occupied


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
    )
    assert process(test_vals) == 37
    puz = Puzzle(2020, 11)

    data = process_input(puz.input_data)

    puz.answer_a = process(data)
    print(f"Part 1: {puz.answer_a}")

    assert process(test_vals, tick=tick_part2) == 26

    puz.answer_b = process(data, tick=tick_part2)
    print(f"Part 2: {puz.answer_b}")
