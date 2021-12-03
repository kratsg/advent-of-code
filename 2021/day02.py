def process_input(data):
    split = data.split()
    actions = split[::2]
    values = list(map(int, split[1::2]))
    return list(zip(actions, values))


def part1(sequence):
    horizontal = 0
    depth = 0
    for action, value in sequence:
        if action == "forward":
            horizontal += value
        elif action == "down":
            depth += value
        elif action == "up":
            depth -= value
    return horizontal, depth


def part2(sequence):
    horizontal = 0
    depth = 0
    aim = 0
    for action, value in sequence:
        if action == "forward":
            horizontal += value
            depth += aim * value
        elif action == "down":
            aim += value
        elif action == "up":
            aim -= value

    return horizontal, depth


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """forward 5
down 5
forward 8
up 3
down 8
forward 2"""
    )

    assert part1(test_vals) == (15, 10)

    puz = Puzzle(2021, 2)

    data = process_input(puz.input_data)

    part1_h, part1_d = part1(data)

    puz.answer_a = part1_h * part1_d
    print(f"Part 1: {puz.answer_a}")

    assert part2(test_vals) == (15, 60)

    part2_h, part2_d = part2(data)

    puz.answer_b = part2_h * part2_d
    print(f"Part 2: {puz.answer_b}")
