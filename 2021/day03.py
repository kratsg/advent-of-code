def process_input(data):
    return data.split()


def get_rates(items):
    gamma_rate = ""
    epsilon_rate = ""
    for column in zip(*items):
        total = len(column)
        ones = column.count("1")
        zeros = total - ones
        gamma_rate += "1" if ones >= zeros else "0"
        epsilon_rate += "0" if ones >= zeros else "1"
    return gamma_rate, epsilon_rate


def get_gas_rate(items, mode):
    remaining_items = [*items]
    i = 0
    while len(remaining_items) > 1:
        comparator = get_rates(remaining_items)[mode][i]
        remaining_items = [item for item in remaining_items if item[i] == comparator]
        i += 1
    return remaining_items.pop()


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
    )

    test_rates = get_rates(test_vals)
    assert test_rates == ("10110", "01001")
    assert list(map(lambda x: int(x, 2), test_rates)) == [22, 9]

    puz = Puzzle(2021, 3)

    data = process_input(puz.input_data)

    rates = get_rates(data)

    puz.answer_a = int(rates[0], 2) * int(rates[1], 2)
    print(f"Part 1: {puz.answer_a}")

    assert get_gas_rate(test_vals, 0) == "10111"
    assert get_gas_rate(test_vals, 1) == "01010"

    rate_o2 = get_gas_rate(data, 0)
    rate_co2 = get_gas_rate(data, 1)

    puz.answer_b = int(rate_o2, 2) * int(rate_co2, 2)
    print(f"Part 2: {puz.answer_b}")
