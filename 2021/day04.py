import numpy as np


def process_input(data):
    raw_data = data.split()

    numbers = list(map(int, raw_data[0].split(",")))
    cards = np.array(raw_data[1:], dtype="int64")
    return numbers, cards


def play_bingo(numbers, cards, strat="good"):
    mask = np.full(cards.shape, False)
    cards = np.ma.array(cards, mask=mask)

    boards_remaining = set(range(cards.size // 25))

    for number in numbers:
        cards = np.ma.masked_where(cards == number, cards)

        bingo_row = np.where(
            np.sum(cards.mask.reshape(-1, 5, 5), axis=1).reshape(-1) == 5
        )[0]
        bingo_col = np.where(
            np.sum(cards.mask.reshape(-1, 5, 5), axis=2).reshape(-1) == 5
        )[0]

        new_boards_remaining = (
            boards_remaining - set(bingo_row // 5) - set(bingo_col // 5)
        )

        if strat == "good":
            if bingo_row.size > 0:
                return cards, number, int(bingo_row // 5)
            if bingo_col.size > 0:
                return cards, number, int(bingo_col // 5)

        if strat == "bad":
            if len(boards_remaining) == 1:
                if len(new_boards_remaining) == 0:
                    return cards, number, boards_remaining.pop()
        boards_remaining = new_boards_remaining


def score(cards, number, board_idx):
    return cards.reshape(-1, 5, 5)[board_idx].sum() * number


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
    )

    cards, number, board_idx = play_bingo(*test_vals)

    assert cards.reshape(-1, 5, 5)[board_idx].sum() == 188
    assert number == 24
    assert board_idx == 2
    assert score(cards, number, board_idx) == 4512

    puz = Puzzle(2021, 4)

    data = process_input(puz.input_data)
    cards, number, board_idx = play_bingo(*data)

    puz.answer_a = score(cards, number, board_idx)
    print(f"Part 1: {puz.answer_a}")

    cards, number, board_idx = play_bingo(*test_vals, strat="bad")
    assert board_idx == 1
    assert cards.reshape(-1, 5, 5)[board_idx].sum() == 148
    assert score(cards, number, board_idx) == 1924

    cards, number, board_idx = play_bingo(*data, strat="bad")

    puz.answer_b = score(cards, number, board_idx)
    print(f"Part 2: {puz.answer_b}")
