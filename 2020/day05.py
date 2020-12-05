def process_input(data):
    return data.split("\n")


# returns (row, col)
def boarding_pass_to_int(boarding_pass):
    boarding_pass = (
        boarding_pass.replace("F", "0")
        .replace("B", "1")
        .replace("L", "0")
        .replace("R", "1")
    )
    fb = boarding_pass[:-3]
    lr = boarding_pass[-3:]
    return (int(fb, 2), int(lr, 2))


def get_id(row, col):
    return row * 8 + col


if __name__ == "__main__":
    from aocd.models import Puzzle

    assert boarding_pass_to_int("FBFBBFFRLR") == (44, 5)
    assert get_id(44, 5) == 357
    assert boarding_pass_to_int("BFFFBBFRRR") == (70, 7)
    assert get_id(70, 7) == 567
    assert boarding_pass_to_int("FFFBBBFRRR") == (14, 7)
    assert get_id(14, 7) == 119
    assert boarding_pass_to_int("BBFFBBFRLL") == (102, 4)
    assert get_id(102, 4) == 820

    puz = Puzzle(2020, 5)

    data = process_input(puz.input_data)

    all_ids = sorted(map(lambda x: get_id(*boarding_pass_to_int(x)), data))

    puz.answer_a = all_ids[-1]
    print(f"Part 1: {puz.answer_a}")

    for left, right in zip(all_ids, all_ids[1:]):
        if right - left == 2:
            break

    puz.answer_b = left + 1
    print(f"Part 2: {puz.answer_b}")
