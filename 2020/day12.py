def process_input(data):
    return list(map(lambda x: (x[0], int(x[1:])), data.split()))


def manhattan(position):
    return int(sum([abs(position.real), abs(position.imag)]))


def tick(coord, action, value, step=0 + 0j):
    if action == "F":
        return coord + value * step
    elif action == "N":
        return coord + value * 1j
    elif action == "S":
        return coord + value * -1j
    elif action == "E":
        return coord + value * 1
    elif action == "W":
        return coord + value * -1
    elif action == "L":
        return coord * ((1j) ** (value // 90))
    elif action == "R":
        return coord * ((-1j) ** (value // 90))


def move(actions):
    position = 0 + 0j
    direction = 1 + 0j

    for action, value in actions:
        if action in "FNSEW":
            position = tick(position, action, value, step=direction)
        elif action in "LR":
            direction = tick(direction, action, value)
    return position


def move_waypoint(actions):
    position = 0 + 0j
    waypoint = 10 + 1j

    for action, value in actions:
        if action in "F":
            position = tick(position, action, value, step=waypoint)
        elif action in "NSEWLR":
            waypoint = tick(waypoint, action, value)
    return position


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """F10
N3
F7
R90
F11"""
    )
    assert move(test_vals) == 17 - 8j
    assert manhattan(move(test_vals)) == 25

    puz = Puzzle(2020, 12)

    data = process_input(puz.input_data)

    puz.answer_a = manhattan(move(data))
    print(f"Part 1: {puz.answer_a}")

    assert manhattan(move_waypoint(test_vals)) == 286

    puz.answer_b = manhattan(move_waypoint(data))
    print(f"Part 2: {puz.answer_b}")
