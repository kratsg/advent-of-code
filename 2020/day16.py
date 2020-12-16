import re
import operator
import functools

pattern_range = re.compile("(?P<min>\d+)-(?P<max>\d+)")


def process_input(data):
    rules = {}
    tickets = {"mine": (), "nearby": []}

    doRules = True
    doYourTicket = False
    for line in data.split("\n"):
        line = line.strip()
        if not line:
            continue

        if line.startswith("your ticket"):
            doRules = False
            doYourTicket = True
            continue
        if line.startswith("nearby tickets"):
            doYourTicket = False
            continue

        if doRules:
            field, rule = line.split(": ")
            rule = map(lambda x: map(int, x), pattern_range.findall(rule))
            rules.setdefault(field, [])
            for lo, hi in rule:
                rules[field].extend(range(lo, hi + 1))  # note inclusive
            continue

        ticket = list(map(int, line.split(",")))
        if doYourTicket:
            tickets["mine"] = ticket
        else:
            tickets["nearby"].append(ticket)
    return (rules, tickets)


def reduce_rules(rules):
    # copy
    rules = [*rules]
    valid_rules = [None] * len(rules)
    while None in valid_rules:
        for index, ruleset in enumerate(rules):
            if len(ruleset) == 0:
                continue
            if len(ruleset) == 1:
                valid_rules[index] = ruleset[0]
            rules[index] = [r for r in ruleset if r not in valid_rules]
    return valid_rules


def find_invalid_value(rulevalues, ticket):
    for ticketvalue in ticket:
        if all(ticketvalue not in rulevalue for rulevalue in rulevalues):
            return ticketvalue
    return None


def find_valid_rules(rules, ticketsvalues):
    for rule, rulevalues in rules.items():
        if find_invalid_value([rulevalues], ticketsvalues) is None:
            yield rule


def find_ordering(rules, tickets):
    valid = []
    current_rules = {**rules}
    for ticketsvalues in zip(*tickets):
        valid_rules = list(find_valid_rules(current_rules, ticketsvalues))
        valid.append(valid_rules)

    return reduce_rules(valid)


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    )
    test_rules, test_tickets = test_vals
    assert find_invalid_value(test_rules.values(), test_tickets["mine"]) is None
    assert find_invalid_value(test_rules.values(), test_tickets["nearby"][0]) is None
    assert find_invalid_value(test_rules.values(), test_tickets["nearby"][1]) == 4
    assert find_invalid_value(test_rules.values(), test_tickets["nearby"][2]) == 55
    assert find_invalid_value(test_rules.values(), test_tickets["nearby"][3]) == 12

    test_invalid_values = [
        find_invalid_value(test_rules.values(), ticket)
        for ticket in test_tickets["nearby"]
    ]
    assert sum(x for x in test_invalid_values if x is not None) == 71

    puz = Puzzle(2020, 16)

    data = process_input(puz.input_data)
    rules, tickets = data

    invalid_values = [
        find_invalid_value(rules.values(), ticket) for ticket in tickets["nearby"]
    ]
    puz.answer_a = sum(x for x in invalid_values if x is not None)
    print(f"Part 1: {puz.answer_a}")

    test_vals2 = process_input(
        """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""
    )
    test_rules2, test_tickets2 = test_vals2
    test_ordering = find_ordering(test_rules2, test_tickets2["nearby"])
    assert len(test_ordering) == len(test_rules2)
    assert test_ordering == ["row", "class", "seat"]

    test_my_ticket = dict(zip(test_ordering, test_tickets2["mine"]))
    assert test_my_ticket["class"] == 12
    assert test_my_ticket["row"] == 11
    assert test_my_ticket["seat"] == 13

    # remove invalid tickets
    tickets["nearby"] = [
        ticket
        for ticket in tickets["nearby"]
        if find_invalid_value(rules.values(), ticket) is None
    ]

    ordering = find_ordering(rules, tickets["nearby"])
    assert len(ordering) == len(rules)
    my_ticket = dict(zip(ordering, tickets["mine"]))
    puz.answer_b = functools.reduce(
        operator.mul,
        [value for field, value in my_ticket.items() if field.startswith("departure")],
    )
    print(f"Part 2: {puz.answer_b}")
