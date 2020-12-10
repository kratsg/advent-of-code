def process_input(data):
    return [0] + sorted(map(int, data.split()))


def get_diffs(data):
    return [t - s for s, t in zip(data, data[1:])]


def get_rating(data):
    return data[-1] + 3


def count_permutations(data):
    rating = get_rating(data)
    ways = [1] + [0] * rating
    for value in data[1:] + [rating]:
        ways[value] = ways[value - 3] + ways[value - 2] + ways[value - 1]
    return ways[-1]


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """16
10
15
5
1
11
7
19
6
12
4"""
    )
    assert get_rating(test_vals) == 22

    test_vals2 = process_input(
        """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
    )
    diffs = get_diffs(test_vals2)
    assert diffs.count(1) == 22
    assert diffs.count(3) + 1 == 10
    puz = Puzzle(2020, 10)

    data = process_input(puz.input_data)
    diffs = get_diffs(data)
    puz.answer_a = diffs.count(1) * (diffs.count(3) + 1)
    print(f"Part 1: {puz.answer_a}")

    assert count_permutations(test_vals) == 8
    assert count_permutations(test_vals2) == 19208
    puz.answer_b = count_permutations(data)
    print(f"Part 2: {puz.answer_b}")
