def process_input(data):
    return list(map(lambda x: list(map(int, x.split("\n")[1:])), data.split("\n\n")))


def play_part1(player1, player2):
    player1, player2 = [*player1], [*player2]
    while player1 and player2:
        p1 = player1.pop(0)
        p2 = player2.pop(0)
        if p1 > p2:
            player1.extend([p1, p2])
        else:
            player2.extend([p2, p1])
    return [player1, player2]


def stringify(player1, player2):
    return "|".join(map(lambda x: ",".join(map(str, x)), [player1, player2]))


def play_part2(player1, player2, depth=0):
    player1, player2 = [*player1], [*player2]
    history = {}
    while player1 and player2:
        winner = None
        string = stringify(player1, player2)

        if string in history:
            return "p1"
        history[stringify(player1, player2)] = True
        p1 = player1.pop(0)
        p2 = player2.pop(0)

        if p1 <= len(player1) and p2 <= len(player2):
            winner = play_part2(player1[:p1], player2[:p2], depth=depth + 1)
        elif p1 > p2:
            winner = "p1"
        else:
            winner = "p2"

        if winner == "p1":
            player1.extend([p1, p2])
        elif winner == "p2":
            player2.extend([p2, p1])
    if depth == 0:
        return [player1, player2]
    else:
        return "p1" if player1 else "p2"


def calculate_scores(player1, player2):
    return list(
        map(
            lambda cards: sum(i * c for i, c in enumerate(cards[::-1], 1)),
            [player1, player2],
        )
    )


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
    )
    assert test_vals == [[9, 2, 6, 3, 1], [5, 8, 4, 7, 10]]
    test_final = play_part1(*test_vals)
    assert test_vals == [[9, 2, 6, 3, 1], [5, 8, 4, 7, 10]]
    assert test_final == [[], [3, 2, 10, 6, 8, 5, 9, 4, 7, 1]]
    assert calculate_scores(*test_final) == [0, 306]

    puz = Puzzle(2020, 22)

    data = process_input(puz.input_data)
    final = play_part1(*data)
    scores = calculate_scores(*final)
    puz.answer_a = max(scores)
    print(f"Part 1: {puz.answer_a}")

    test_final2 = play_part2(*test_vals)
    assert test_vals == [[9, 2, 6, 3, 1], [5, 8, 4, 7, 10]]
    assert test_final2 == [[], [7, 5, 6, 2, 4, 1, 10, 8, 9, 3]]
    assert calculate_scores(*test_final2) == [0, 291]

    final2 = play_part2(*data)
    scores2 = calculate_scores(*final2)
    puz.answer_b = max(scores2)
    print(f"Part 2: {puz.answer_b}")
