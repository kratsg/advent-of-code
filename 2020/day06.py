def process_input(data):
    return data.replace("\n\n", "|").replace("\n", ",").split("|")


def group_count(group_data):
    return len(set(group_data.replace(",", "")))


def group_total_count(group_data):
    users = group_data.split(",")
    first_user = set(users[0])
    if len(users) == 1:
        return len(first_user)
    rest = map(set, users[1:])
    return len(first_user.intersection(*rest))


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """abcx
abcy
abcz"""
    )

    assert len(test_vals) == 1
    assert group_count(test_vals[0]) == 6

    test_vals2 = process_input(
        """abc

a
b
c

ab
ac

a
a
a
a

b"""
    )
    assert len(test_vals2) == 5
    assert group_count(test_vals2[0]) == 3
    assert group_count(test_vals2[1]) == 3
    assert group_count(test_vals2[2]) == 3
    assert group_count(test_vals2[3]) == 1
    assert group_count(test_vals2[4]) == 1

    puz = Puzzle(2020, 6)

    data = process_input(puz.input_data)
    counts = list(map(group_count, data))

    puz.answer_a = sum(counts)
    print(f"Part 1: {puz.answer_a}")

    assert group_total_count(test_vals2[0]) == 3
    assert group_total_count(test_vals2[1]) == 0
    assert group_total_count(test_vals2[2]) == 1
    assert group_total_count(test_vals2[3]) == 1
    assert group_total_count(test_vals2[4]) == 1

    total_counts = list(map(group_total_count, data))

    puz.answer_b = sum(total_counts)
    print(f"Part 2: {puz.answer_b}")
