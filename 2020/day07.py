import re

pattern = re.compile(
    "^(?P<outer_bag>.*?) bags? contain (?P<empty>no other bags)?\s?(?P<inner_bags>.*?)?\.$"
)
bags_split = re.compile("(?P<quantity>\d)?\s?(?P<color>[a-zA-Z\s]+?) bags?")


def process_input(data):
    results = []
    for line in data.split("\n"):
        match = pattern.match(line)
        results.append(match.groupdict())
        results[-1]["inner_bags"] = list(
            map(
                lambda x: x.groupdict() if x else x,
                bags_split.finditer(results[-1]["inner_bags"]),
            )
        )
    return results


def make_rules(data):
    rules = {}
    for rule in data:
        rules[rule["outer_bag"]] = {
            "empty": rule["empty"] is not None,
            "inner_bags": {},
        }
        for inner_bag in rule["inner_bags"]:
            rules[rule["outer_bag"]]["inner_bags"][inner_bag["color"]] = int(
                inner_bag["quantity"]
            )
    return rules


def can_contain(bag, outer_bag, rules):
    if rules[outer_bag]["empty"]:
        return False
    if bag in rules[outer_bag]["inner_bags"]:
        return True
    result = False
    for inner_bag in rules[outer_bag]["inner_bags"].keys():
        if can_contain(bag, inner_bag, rules):
            return True
    return False


def count_outer_bag(bag, rules):
    total = 0
    for outer_bag in rules.keys():
        total += can_contain(bag, outer_bag, rules)

    return total


def count_inner_bags(outer_bag, rules):
    total = 0
    if rules[outer_bag]["empty"]:
        return total
    for inner_bag, quantity in rules[outer_bag]["inner_bags"].items():
        total += quantity
        total += quantity * count_inner_bags(inner_bag, rules)
    return total


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
    )
    assert test_vals[0] == {
        "outer_bag": "light red",
        "empty": None,
        "inner_bags": [
            {"quantity": "1", "color": "bright white"},
            {"quantity": "2", "color": "muted yellow"},
        ],
    }
    assert test_vals[1] == {
        "outer_bag": "dark orange",
        "empty": None,
        "inner_bags": [
            {"quantity": "3", "color": "bright white"},
            {"quantity": "4", "color": "muted yellow"},
        ],
    }
    assert test_vals[2] == {
        "outer_bag": "bright white",
        "empty": None,
        "inner_bags": [{"quantity": "1", "color": "shiny gold"}],
    }
    assert test_vals[3] == {
        "outer_bag": "muted yellow",
        "empty": None,
        "inner_bags": [
            {"quantity": "2", "color": "shiny gold"},
            {"quantity": "9", "color": "faded blue"},
        ],
    }
    assert test_vals[4] == {
        "outer_bag": "shiny gold",
        "empty": None,
        "inner_bags": [
            {"quantity": "1", "color": "dark olive"},
            {"quantity": "2", "color": "vibrant plum"},
        ],
    }
    assert test_vals[5] == {
        "outer_bag": "dark olive",
        "empty": None,
        "inner_bags": [
            {"quantity": "3", "color": "faded blue"},
            {"quantity": "4", "color": "dotted black"},
        ],
    }
    assert test_vals[6] == {
        "outer_bag": "vibrant plum",
        "empty": None,
        "inner_bags": [
            {"quantity": "5", "color": "faded blue"},
            {"quantity": "6", "color": "dotted black"},
        ],
    }
    assert test_vals[7] == {
        "outer_bag": "faded blue",
        "empty": "no other bags",
        "inner_bags": [],
    }
    assert test_vals[8] == {
        "outer_bag": "dotted black",
        "empty": "no other bags",
        "inner_bags": [],
    }

    test_rules = make_rules(test_vals)
    assert test_rules["light red"] == {
        "empty": False,
        "inner_bags": {"bright white": 1, "muted yellow": 2},
    }
    assert test_rules["dark orange"] == {
        "empty": False,
        "inner_bags": {"bright white": 3, "muted yellow": 4},
    }
    assert test_rules["bright white"] == {
        "empty": False,
        "inner_bags": {"shiny gold": 1},
    }
    assert test_rules["muted yellow"] == {
        "empty": False,
        "inner_bags": {"shiny gold": 2, "faded blue": 9},
    }
    assert test_rules["shiny gold"] == {
        "empty": False,
        "inner_bags": {"dark olive": 1, "vibrant plum": 2},
    }
    assert test_rules["dark olive"] == {
        "empty": False,
        "inner_bags": {"faded blue": 3, "dotted black": 4},
    }
    assert test_rules["vibrant plum"] == {
        "empty": False,
        "inner_bags": {"faded blue": 5, "dotted black": 6},
    }
    assert test_rules["faded blue"] == {"empty": True, "inner_bags": {}}
    assert test_rules["dotted black"] == {"empty": True, "inner_bags": {}}

    assert can_contain("shiny gold", "light red", test_rules)
    assert can_contain("shiny gold", "dark orange", test_rules)
    assert can_contain("shiny gold", "bright white", test_rules)
    assert can_contain("shiny gold", "muted yellow", test_rules)
    assert not can_contain("shiny gold", "shiny gold", test_rules)
    assert not can_contain("shiny gold", "dark olive", test_rules)
    assert not can_contain("shiny gold", "vibrant plum", test_rules)
    assert not can_contain("shiny gold", "faded blue", test_rules)
    assert not can_contain("shiny gold", "dotted black", test_rules)

    assert count_outer_bag("shiny gold", test_rules) == 4

    puz = Puzzle(2020, 7)

    data = process_input(puz.input_data)
    rules = make_rules(data)

    puz.answer_a = count_outer_bag("shiny gold", rules)
    print(f"Part 1: {puz.answer_a}")

    assert count_inner_bags("dark olive", test_rules) == 7
    assert count_inner_bags("vibrant plum", test_rules) == 11
    assert count_inner_bags("shiny gold", test_rules) == 32
    test_vals2 = process_input(
        """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""
    )
    test_rules2 = make_rules(test_vals2)
    assert count_inner_bags("shiny gold", test_rules2) == 126

    puz.answer_b = count_inner_bags("shiny gold", rules)
    print(f"Part 2: {puz.answer_b}")
