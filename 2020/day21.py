import re
import functools


def process_input(data):
    results = []
    for line in data.split("\n"):
        line = re.sub("[^a-z ]", "", line)
        ingredients, allergens = map(lambda x: x.split(" "), line.split(" contains "))
        results.append((set(ingredients), set(allergens)))
    return results


def get_all_ingredients(recipes):
    return functools.reduce(lambda x, y: x.union(y), [k for k, _ in recipes])


def get_all_allergens(recipes):
    return functools.reduce(lambda x, y: x.union(y), [k for _, k in recipes])


def matching(recipes):
    matched = {}
    all_allergens = get_all_allergens(recipes)
    for allergen in all_allergens:
        matched_ingredients = None
        for ingredients, allergens in recipes:
            if allergen not in allergens:
                continue
            if matched_ingredients is None:
                matched_ingredients = ingredients
                continue
            matched_ingredients = matched_ingredients.intersection(ingredients)
        matched[allergen] = matched_ingredients
    return matched


def no_allergens(recipes, matched):
    all_ingredients = get_all_ingredients(recipes)
    return all_ingredients - set(j for i in matched.values() for j in i)


def count_ingredients(recipes, ingredients):
    count = 0
    for recipe in recipes:
        count += len(recipe[0].intersection(ingredients))
    return count


def reduce_rules(rules):
    # copy
    rules = {**rules}
    valid_rules = {k: None for k in rules}
    while None in valid_rules.values():
        for index, (ingredient, ruleset) in enumerate(list(rules.items())):
            if len(ruleset) == 0:
                continue
            if len(ruleset) == 1:
                valid_rules[ingredient] = ruleset
                del rules[ingredient]
                for ingredient, allergens in rules.items():
                    rules[ingredient] = allergens - ruleset
    return {list(v)[0]: k for k, v in valid_rules.items()}


def to_string(reduced):
    return ",".join(k for k, v in sorted(reduced.items(), key=lambda x: x[1]))


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
    )
    test_matched = matching(test_vals)
    test_no_match = no_allergens(test_vals, test_matched)
    assert count_ingredients(test_vals, test_no_match) == 5

    puz = Puzzle(2020, 21)

    data = process_input(puz.input_data)
    matched = matching(data)
    no_match = no_allergens(data, matched)
    puz.answer_a = count_ingredients(data, no_match)
    print(f"Part 1: {puz.answer_a}")

    test_reduced = reduce_rules(test_matched)
    assert to_string(test_reduced) == "mxmxvkd,sqjhc,fvjkl"

    reduced = reduce_rules(matched)
    puz.answer_b = to_string(reduced)
    print(f"Part 2: {puz.answer_b}")
