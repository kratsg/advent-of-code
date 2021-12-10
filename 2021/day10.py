import numpy as np


def process_input(data):
    return data.splitlines()


def valid_chunk(line):
    matcher = {"(": ")", "{": "}", "[": "]", "<": ">"}

    groups = []
    try:
        for char in line:
            if char in matcher:
                groups.append(matcher[char])
            else:
                assert char == groups.pop()
    except AssertionError:
        # reminder to reverse groups in order of what is needed next
        return False, char, groups[::-1]

    if len(groups):
        # reminder to reverse groups in order of what is needed next
        return False, "incomplete", groups[::-1]

    return True, "ok", groups


def calculate_error(result):
    return {")": 3, "]": 57, "}": 1197, ">": 25137}.get(result[1], 0)


def calculate_autocomplete(groups):
    total = 0
    for char in groups:
        total *= 5
        total += 1 + ")]}>".index(char)
    return total


def parts(lines):
    part1 = 0
    part2 = []
    for line in lines:
        result = valid_chunk(line)
        value = calculate_error(result)
        part1 += value
        # corrupt
        if value != 0:
            continue
        # no problem on line
        if result[0]:
            continue
        # incomplete lines only
        *_, groups = result

        part2.append(calculate_autocomplete(groups))

    return part1, part2


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
    )

    assert valid_chunk(test_vals[0])[0] == False
    assert valid_chunk(test_vals[1])[0] == False
    assert valid_chunk(test_vals[2])[0] == False
    assert valid_chunk(test_vals[3])[0] == False
    assert valid_chunk(test_vals[4])[0] == False
    assert valid_chunk(test_vals[5])[0] == False
    assert valid_chunk(test_vals[6])[0] == False
    assert valid_chunk(test_vals[7])[0] == False
    assert valid_chunk(test_vals[8])[0] == False
    assert valid_chunk(test_vals[9])[0] == False

    test_part1, test_part2 = parts(test_vals)
    assert test_part1 == 26397

    puz = Puzzle(2021, 10)

    data = process_input(puz.input_data)

    part1, part2 = parts(data)

    puz.answer_a = part1
    print(f"Part 1: {puz.answer_a}")

    assert calculate_autocomplete(list("}}]])})]")) == 288957
    assert calculate_autocomplete(list(")}>]})")) == 5566
    assert calculate_autocomplete(list("}}>}>))))")) == 1480781
    assert calculate_autocomplete(list("]]}}]}]}>")) == 995444
    assert calculate_autocomplete(list("])}>")) == 294
    assert sorted(test_part2)[len(test_part2) // 2] == 288957

    puz.answer_b = sorted(part2)[len(part2) // 2]
    print(f"Part 2: {puz.answer_b}")
