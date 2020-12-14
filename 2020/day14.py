import re

pattern = re.compile("^mem\[(?P<address>\d+)\] = (?P<value>\d+)$")


def process_input(data):
    # [{'mask': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 'inst': [{'address': '8', 'value': '11'}, {'address': '7', 'value': '101'}, {'address': '8', 'value': '0'}]}]
    results = []
    for line in data.splitlines():
        if line.startswith("mask"):
            results.append({"mask": line.split("=")[-1].strip(), "inst": []})
            continue

        matches = pattern.search(line)
        results[-1]["inst"].append(matches.groupdict())
    return results


def apply_mask(mask, value):
    value = f"{int(value):b}".zfill(36)
    return int("".join(v if m == "X" else m for m, v in zip(mask, value)), 2)


def apply_mask_part2(mask, addr):
    addr = f"{int(addr):b}".zfill(36)
    floating_addr = "".join(
        a if m == "0" else ("1" if m == "1" else "X") for m, a in zip(mask, addr)
    )
    num_floats = floating_addr.count("X")
    for i in range(2 ** num_floats):

        def callback(match):
            return next(callback.replace)

        callback.replace = iter(f"{int(i):b}".zfill(num_floats))
        yield int(re.sub(r"X", callback, floating_addr), 2)


def compute(data):
    memory = {}
    for group in data:
        mask = group["mask"]
        for inst in group["inst"]:
            memory[int(inst["address"])] = apply_mask(mask, inst["value"])
    return memory


def compute_part2(data):
    memory = {}
    for group in data:
        mask = group["mask"]
        for inst in group["inst"]:
            addresses = apply_mask_part2(mask, inst["address"])
            value = int(inst["value"])
            for address in addresses:
                memory[address] = value
    return memory


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
    )

    test_memory = compute(test_vals)
    assert test_memory == {7: 101, 8: 64}
    assert sum(test_memory.values()) == 165

    puz = Puzzle(2020, 14)

    data = process_input(puz.input_data)
    memory = compute(data)

    puz.answer_a = sum(memory.values())
    print(f"Part 1: {puz.answer_a}")

    test_vals2 = process_input(
        """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
    )
    test_memory2 = compute_part2(test_vals2)
    assert test_memory2 == {
        26: 1,
        27: 1,
        58: 100,
        59: 100,
        16: 1,
        17: 1,
        18: 1,
        19: 1,
        24: 1,
        25: 1,
    }
    assert sum(test_memory2.values()) == 208

    memory2 = compute_part2(data)
    puz.answer_b = sum(memory2.values())
    print(f"Part 2: {puz.answer_b}")
