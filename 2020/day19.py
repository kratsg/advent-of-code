import functools
import operator
import re


rule_pattern = re.compile("""(?P<index>\d+): (?P<pattern>.*)""")


def process_input(data, substitutions={}):
    results = {"rules": {}, "data": []}
    to_parse = {}
    for line in data.split("\n"):
        line = line.strip()
        if not line:
            continue
        rule = rule_pattern.match(line)
        if not rule:
            results["data"].append(line)
            continue

        rule_dict = rule.groupdict()
        index = rule_dict["index"]
        pattern = rule_dict["pattern"]
        pattern = pattern.replace('"', "")

        pattern = substitutions.get(index, pattern)

        if len(pattern) == 1:
            to_parse[index] = [pattern]
        else:
            to_parse[index] = [i.strip() for i in pattern.split("|")]
    while to_parse:
        for k in list(to_parse.keys()):
            v = to_parse[k]

            v = [
                " ".join(results["rules"].get(i, i) for i in subset.split(" "))
                for subset in v
            ]

            if not any(map(lambda x: any([str.isdigit(i) for i in x]), v)):
                new_rule = "|".join(v).replace(" ", "")
                if len(new_rule) > 1:
                    new_rule = f"({new_rule})"
                results["rules"][k] = new_rule
                del to_parse[k]
            else:
                to_parse[k] = v

    return results


def count_valid(rule, data):
    pattern = re.compile(rule)
    return sum(bool(pattern.fullmatch(message)) for message in data)


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_rules = process_input(
        """0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b" """
    )
    assert test_rules["rules"] == {
        "1": "a",
        "3": "b",
        "2": "(ab|ba)",
        "0": "(a(ab|ba))",
    }

    test_vals = process_input(
        """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
    )
    assert count_valid(test_vals["rules"]["0"], test_vals["data"]) == 2

    puz = Puzzle(2020, 19)

    data = process_input(puz.input_data)

    puz.answer_a = count_valid(data["rules"]["0"], data["data"])
    print(f"Part 1: {puz.answer_a}")

    # honestly, just do it n times
    # 8: 42 | 42 8 == 8: 42+
    # 11: 42 31 | 42 11 31 == 11: 42{n} 31{n}
    substitutions = {
        "8": "42 +",
        "11": " | ".join(
            map(
                lambda x: " ".join(x),
                zip(*([" ".join([x] * i) for i in range(1, 10)] for x in ["42", "31"])),
            )
        ),
    }
    test_vals2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

    test_data = process_input(test_vals2)
    assert count_valid(test_data["rules"]["0"], test_data["data"]) == 3
    test_data2 = process_input(test_vals2, substitutions)
    assert count_valid(test_data2["rules"]["0"], test_data2["data"]) == 12

    data = process_input(puz.input_data, substitutions)

    puz.answer_b = count_valid(data["rules"]["0"], data["data"])
    print(f"Part 2: {puz.answer_b}")
