import re
import functools
import collections
import operator
import copy


class Location:
    def __init__(self, x, y, z):
        self.values = (x, y, z)

    def __add__(self, other):
        return Location(*list(map(sum, zip(self, other))))

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        return f"<Location {self.values}>"

    def __eq__(self, other):
        return self.values == other.values

    def __hash__(self):
        return hash(self.values)


# cube coordinates: https://www.redblobgames.com/grids/hexagons/#coordinates-cube
MOVES = {
    "e": Location(1, -1, 0),
    "w": Location(-1, 1, 0),
    "se": Location(0, -1, 1),
    "sw": Location(-1, 0, 1),
    "ne": Location(1, 0, -1),
    "nw": Location(0, 1, -1),
}

pattern = re.compile("|".join(MOVES.keys()))


def process_input(data):
    return [
        tuple(MOVES.get(i) for i in pattern.findall(line)) for line in data.split("\n")
    ]


def build_grid(movesets):
    grid = set()
    for moveset in movesets:
        position = functools.reduce(operator.add, moveset)
        if position in grid:
            grid.remove(position)
        else:
            grid.add(position)
    return grid


def tick(grid):
    check_tiles = set(grid)

    for tile in grid:
        for move in MOVES.values():
            check_tiles.add(move + tile)

    new_grid = set()
    for tile in check_tiles:
        black_neighbors = sum((move + tile) in grid for move in MOVES.values())
        if tile in grid:
            if black_neighbors in [1, 2]:
                new_grid.add(tile)
        else:
            if black_neighbors == 2:
                new_grid.add(tile)

    return new_grid


def process(grid, ndays=100):
    grid = set(grid)
    for _ in range(ndays):
        grid = tick(grid)
    return grid


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""
    )
    test_grid = build_grid(test_vals)
    assert len(test_grid) == 10

    puz = Puzzle(2020, 24)

    data = process_input(puz.input_data)
    grid = build_grid(data)
    puz.answer_a = len(grid)
    print(f"Part 1: {puz.answer_a}")

    assert len(process(test_grid, 1)) == 15
    assert len(process(test_grid, 2)) == 12
    assert len(process(test_grid, 3)) == 25
    assert len(process(test_grid, 4)) == 14
    assert len(process(test_grid, 5)) == 23
    assert len(process(test_grid, 6)) == 28
    assert len(process(test_grid, 7)) == 41
    assert len(process(test_grid, 8)) == 37
    assert len(process(test_grid, 9)) == 49
    assert len(process(test_grid, 10)) == 37
    assert len(process(test_grid, 20)) == 132
    assert len(process(test_grid, 30)) == 259
    assert len(process(test_grid, 40)) == 406
    assert len(process(test_grid, 50)) == 566
    assert len(process(test_grid, 60)) == 788
    assert len(process(test_grid, 70)) == 1106
    assert len(process(test_grid, 80)) == 1373
    assert len(process(test_grid, 90)) == 1844
    assert len(process(test_grid, 100)) == 2208

    puz.answer_b = len(process(grid, 100))
    print(f"Part 2: {puz.answer_b}")
