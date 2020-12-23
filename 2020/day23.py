def process_input(data):
    return list(map(int, data))


def rotate_to_one(cups):
    index = cups.index(1)
    return cups[index:] + cups[:index]


def stringify(cups, start=1):
    return "".join(map(str, cups[start:]))


def play(cups, nrounds=10):
    cups = [*cups]
    for move in range(nrounds):
        start_cup = cups[0]
        three_cups = cups[1:4]
        rest = cups[4:]

        try:
            closest_cup = min(
                [i for i in rest if i < start_cup], key=lambda x: start_cup - x
            )
        except ValueError:
            # ValueError: min() arg is an empty sequence
            closest_cup = max(rest)

        insert_index = rest.index(closest_cup)
        cups = (
            rest[: insert_index + 1]
            + three_cups
            + rest[insert_index + 1 :]
            + [start_cup]
        )
    return rotate_to_one(cups)


def play_part2(cups, nrounds=10000000, maxcups=1000000):
    start_cup = cups[0]
    cups = cups + list(range(max(cups) + 1, maxcups + 1))
    cups = {**{cup: cups[i + 1] for i, cup in enumerate(cups[:-1])}, cups[-1]: cups[0]}

    for move in range(nrounds):
        three_cups = []

        # get the three cups
        three_cups = [cups[start_cup]]
        three_cups.append(cups[three_cups[-1]])
        three_cups.append(cups[three_cups[-1]])

        # start cup now points to cup after the three
        cups[start_cup] = cups[three_cups[-1]]

        closest_cup = maxcups if start_cup == 1 else start_cup - 1
        while closest_cup in three_cups:
            closest_cup = maxcups if closest_cup == 1 else closest_cup - 1

        # we never changed the following two, so they point correctly
        # cups[three_cups[0]] = three_cups[1]
        # cups[three_cups[1]] = three_cups[2]
        # the last one needs to point at next cup to closest cup
        cups[three_cups[2]] = cups[closest_cup]
        # closest cup needs to point to first
        cups[closest_cup] = three_cups[0]
        start_cup = cups[start_cup]

    return_cups = [1]
    while cups:
        return_cups.append(cups.pop(return_cups[-1]))

    return return_cups[:-1]


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input("""389125467""")
    test_final = play(test_vals)
    assert stringify(test_final) == "92658374"

    test_final = play(test_vals, 100)
    assert stringify(test_final) == "67384529"

    puz = Puzzle(2020, 23)

    data = process_input(puz.input_data)
    final = play(data, 100)
    puz.answer_a = stringify(final)
    print(f"Part 1: {puz.answer_a}")

    assert stringify(play_part2(test_vals, 10, 9)) == "92658374"
    assert stringify(play_part2(test_vals, 100, 9)) == "67384529"
    test_final2 = play_part2(test_vals)
    assert test_final2[1:3] == [934001, 159792]
    assert test_final2[1] * test_final2[2] == 149245887792

    final = play_part2(data)
    puz.answer_b = final[1] * final[2]
    print(f"Part 2: {puz.answer_b}")
