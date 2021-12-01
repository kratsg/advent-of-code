def process_input(data):
    return list(map(int, data.split()))

def moving_window(measurements):
    measurements = (i for i in measurements)
    base = next(measurements)
    try:
        while True:
            differential = next(measurements) - base
            yield 1 if differential > 0 else 0
            base += differential
    except StopIteration:
        pass

def window_sum(measurements):
    for i, base in enumerate(measurements[:-2]):
        yield sum(measurements[i:i+3])

if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """199
200
208
210
200
207
240
269
260
263"""
    )

    assert sum(moving_window(test_vals)) == 7

    puz = Puzzle(2021, 1)

    numbers = list(map(int, puz.input_data.split()))

    puz.answer_a = sum(moving_window(numbers))
    print(f"Part 1: {puz.answer_a}")


    assert sum(moving_window(window_sum(test_vals))) == 5

    puz.answer_b = sum(moving_window(window_sum(numbers)))
    print(f"Part 2: {puz.answer_b}")
