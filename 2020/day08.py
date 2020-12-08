def process_input(data):
    it = iter(data.split())
    return [(x, int(next(it))) for x in it]


def computer(instructions, pointers=None, accumulators=None):
    accumulators = accumulators or [0]
    pointers = pointers or [0]
    while True:
        pointer = pointers[-1]
        accumulator = accumulators[-1]
        instruction, value = instructions[pointer]
        if instruction == "nop":
            pointer += 1
        elif instruction == "acc":
            accumulator += value
            pointer += 1
        elif instruction == "jmp":
            pointer += value

        if pointer in pointers:
            return (False, pointers, accumulators)

        pointers.append(pointer)
        accumulators.append(accumulator)

        if pointer == len(instructions):
            return (True, pointers, accumulators)

    return (False, pointers, accumulators)


def fix_bug(instructions, pointers, accumulators):
    for i in range(1, len(pointers)):
        index = pointers[-i]
        command, value = instructions[index]
        if command not in ["nop", "jmp"]:
            continue

        new_instructions = [*instructions]
        new_instructions[index] = ("nop" if command == "jmp" else "nop", value)
        success, new_pointers, new_accumulators = computer(
            new_instructions, pointers=pointers[:-i], accumulators=accumulators[:-i]
        )
        if success:
            return (success, new_pointers, new_accumulators)

    return (False, pointers, accumulators)


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

    test_success, test_pointers, test_accumulators = computer(test_vals)
    assert test_accumulators[-1] == 5

    puz = Puzzle(2020, 8)

    data = process_input(puz.input_data)

    _, pointers, accumulators = computer(data)

    puz.answer_a = accumulators[-1]
    print(f"Part 1: {puz.answer_a}")

    test_success, test_new_pointers, test_new_accumulators = fix_bug(
        test_vals, test_pointers, test_accumulators
    )
    assert test_success
    assert test_new_accumulators[-1] == 8

    success, new_pointers, new_accumulators = fix_bug(data, pointers, accumulators)
    assert success

    puz.answer_b = new_accumulators[-1]
    print(f"Part 2: {puz.answer_b}")
