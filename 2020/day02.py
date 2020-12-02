import re

pattern = re.compile(
    "^(?P<min>\d+)-(?P<max>\d+) (?P<pattern>[a-z]): (?P<password>\w+$)"
)


def process_input(data):
    lines = []
    for line in data.split("\n"):
        matches = pattern.match(line)
        lines.append(matches.groupdict())
    return lines


def is_password_valid(data, policy="sled"):
    x = int(data["min"])
    y = int(data["max"])
    if policy == "sled":
        count = data["password"].count(data["pattern"])
        return x <= count <= y
    elif policy == "toboggan":
        return (data["password"][x - 1] == data["pattern"]) ^ (
            data["password"][y - 1] == data["pattern"]
        )


def count_valid_passwords(data, policy="sled"):
    total = 0
    for entry in data:
        total += is_password_valid(entry, policy)
    return total


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""
    )
    assert test_vals[0] == {"min": "1", "max": "3", "pattern": "a", "password": "abcde"}
    assert is_password_valid(test_vals[0])
    assert is_password_valid(test_vals[1]) == False
    assert is_password_valid(test_vals[2])
    assert count_valid_passwords(test_vals) == 2

    assert is_password_valid(test_vals[0], policy="toboggan")
    assert is_password_valid(test_vals[1], policy="toboggan") == False
    assert is_password_valid(test_vals[2], policy="toboggan") == False
    assert count_valid_passwords(test_vals, policy="toboggan") == 1

    puz = Puzzle(2020, 2)

    data = process_input(puz.input_data)

    puz.answer_a = count_valid_passwords(data)
    print(f"Part 1: {puz.answer_a}")

    puz.answer_b = count_valid_passwords(data, policy="toboggan")
    print(f"Part 2: {puz.answer_b}")
