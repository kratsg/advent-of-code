import numpy as np
import re

length_to_number = {2: 1, 3: 7, 4: 4, 5: [2, 3, 5], 6: [0, 6, 9], 7: 8}


def process_input(data):
    result = []
    for line in data.splitlines():
        result.append(list(map(lambda x: x.split(" "), line.split(" | "))))
    return result


def get_counts(line):
    return np.array(list(map(len, line)))


def count_unique(lines):
    total = 0
    for digits in lines:
        counts = get_counts(digits[1])
        total += int(np.sum(counts < 5) + np.sum(counts == 7))
    return total


"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
 """


def deduce_line(line):
    left = np.array(line)
    left_counts = get_counts(left)

    deductions = {
        length_to_number[i]: left[left_counts == i][0]
        for i in [2, 3, 4, 7]
        if i in left_counts
    }

    # 0, 6, 9
    for code in left[left_counts == 6]:
        if set(deductions[1]) - set(code):
            # first subtract the code from 1: if there's anything left, definitely a 6
            deductions[6] = code
        elif set(deductions[4]) - set(code):
            # then subtract code from 4: if there's anything left (and it's not a 6), it's a 0
            deductions[0] = code
        else:
            # it's gotta be a 9
            deductions[9] = code

    # 2, 3, 5
    # first compute the 'cc' because i don't know how to differentiate 2/5 otherwise
    cc = set(deductions[1]) - set(deductions[6])
    for code in left[left_counts == 5]:
        if not (set(deductions[1]) - set(code)):
            # subtract the code from 1: if there's nothing left, definitely a 3
            deductions[3] = code
        elif cc - set(code):
            # subtract the code from cc: if anything else, it's a 5
            deductions[5] = code
        else:
            # else it's a 2
            deductions[2] = code

    assert len(deductions) == 10
    # note: frozenset is hashable, so abusing this to look up a number from the (set of) letters
    return {frozenset(code): str(number) for number, code in deductions.items()}


def decode_line(line, deductions):
    return "".join(map(lambda x: deductions[frozenset(x)], line))


def compute_lines(lines):
    total = 0
    for line in lines:
        deductions = deduce_line(line[0])
        total += int(decode_line(line[1], deductions))
    return total


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
    )

    assert count_unique(test_vals) == 26

    puz = Puzzle(2021, 8)

    data = process_input(puz.input_data)

    puz.answer_a = count_unique(data)
    print(f"Part 1: {puz.answer_a}")

    test_val = process_input(
        """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""
    )[0]

    deductions = deduce_line(test_val[0])
    assert decode_line(test_val[1], deductions) == "5353"
    assert compute_lines([test_val]) == 5353

    puz.answer_b = compute_lines(data)
    print(f"Part 2: {puz.answer_b}")
