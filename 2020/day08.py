def process_input(data):
    it = iter(data.split())
    return [(x, int(next(it))) for x in it]


def computer(instructions):
    accumulator = 0
    indices_visited = []
    pointer = 0
    while pointer not in indices_visited:
        instruction, value = instructions[pointer]
        indices_visited.append(pointer)
        if instruction == "nop":
            pointer += 1
        elif instruction == "acc":
            accumulator += value
            pointer += 1
        elif instruction == "jmp":
            pointer += value

        if pointer == len(instructions):
            return (True, accumulator, [])

    return (False, accumulator, indices_visited)


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
    )
    assert len(test_vals) == 9
    assert len(test_vals[0]) == 2

    assert computer(test_vals)[1] == 5

    puz = Puzzle(2020, 8)

    data = process_input(puz.input_data)

    _, accumulator, indices_visited = computer(data)

    puz.answer_a = accumulator
    print(f"Part 1: {puz.answer_a}")

    for index in indices_visited[::-1]:
        instructions = [*data]
        command, value = instructions[index]
        if command in ["nop", "jmp"]:
            instructions[index] = ("nop" if command == "jmp" else "nop", value)
        success, accumulator_part2, _ = computer(instructions)
        if success:
            break

    puz.answer_b = accumulator_part2
    print(f"Part 2: {puz.answer_b}")
