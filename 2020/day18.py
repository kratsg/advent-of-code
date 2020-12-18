import operator
import functools


def process_input(data):
    return data.split("\n")


def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == "(":
            stack.append(i)
        elif c == ")" and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1 : i])


def flat_precedence(expr):
    expr = expr.split()
    total = int(expr[0])
    it = iter(expr[1:])
    for i in it:
        if i == "*":
            total *= int(next(it))
        elif i == "+":
            total += int(next(it))
    return total


def invert_precedence(expr):
    return functools.reduce(operator.mul, map(flat_precedence, expr.split("*")))


def compute(expr, evaluator=flat_precedence):
    substitutions = []
    for level, subexpr in parenthetic_contents(f"({expr})"):
        eval_subexpr = subexpr
        for pattern, replace in substitutions[::-1]:
            eval_subexpr = eval_subexpr.replace(f"({pattern})", f"{replace}")

        computed = evaluator(eval_subexpr)
        if level == 0:
            return computed
        substitutions.append((subexpr, computed))


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""
    )

    assert compute("1 + 2 * 3 + 4 * 5 + 6") == 71
    assert compute("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert compute(test_vals[0]) == 26
    assert compute(test_vals[1]) == 437
    assert compute(test_vals[2]) == 12240
    assert compute(test_vals[3]) == 13632

    puz = Puzzle(2020, 18)

    data = process_input(puz.input_data)

    puz.answer_a = sum(compute(expr) for expr in data)
    print(f"Part 1: {puz.answer_a}")

    assert compute("1 + 2 * 3 + 4 * 5 + 6", invert_precedence) == 231
    assert compute("1 + (2 * 3) + (4 * (5 + 6))", invert_precedence) == 51
    assert compute(test_vals[0], invert_precedence) == 46
    assert compute(test_vals[1], invert_precedence) == 1445
    assert compute(test_vals[2], invert_precedence) == 669060
    assert compute(test_vals[3], invert_precedence) == 23340

    puz.answer_b = sum(compute(expr, invert_precedence) for expr in data)
    print(f"Part 2: {puz.answer_b}")
