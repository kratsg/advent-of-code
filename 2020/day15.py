def process_input(data):
    return list(map(int, data.split(",")))


def count(numbers, total=2020):
    history = {n: i + 1 for i, n in enumerate(numbers[:-1])}
    while len(numbers) < total:
        # get last number spoken
        last_number = numbers[-1]
        # get last time last number was spoken
        last_spoken = history.get(last_number, -1)
        # update the last number's turn to last turn
        last_turn = len(numbers)
        history[last_number] = last_turn
        # new number spoken is 0 unless it was spoken before
        new_number = 0
        if last_spoken > 0:
            # new number is the age (how many turns apart)
            new_number = last_turn - last_spoken
        # speak the new number
        numbers.append(new_number)
    return numbers[-1]


if __name__ == "__main__":
    from aocd.models import Puzzle

    assert count(process_input("0,3,6"), 10) == 0
    assert count(process_input("0,3,6")) == 436
    assert count(process_input("1,3,2")) == 1
    assert count(process_input("2,1,3")) == 10
    assert count(process_input("1,2,3")) == 27
    assert count(process_input("2,3,1")) == 78
    assert count(process_input("3,2,1")) == 438
    assert count(process_input("3,1,2")) == 1836

    puz = Puzzle(2020, 15)

    data = process_input(puz.input_data)

    puz.answer_a = count(data)
    print(f"Part 1: {puz.answer_a}")

    puz.answer_b = count(data, total=30000000)
    print(f"Part 2: {puz.answer_b}")
