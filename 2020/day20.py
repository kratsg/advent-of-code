from io import StringIO
import numpy as np
import collections
import functools
import operator
import re
import itertools

# top right bottom left (like CSS)
def get_edges(tile, add_flips=True):
    edges = [(1, tile[0, :]), (2, tile[:, -1]), (3, tile[-1, :]), (4, tile[:, 0])]
    edges = [("".join(e), i) for i, e in edges]
    if not add_flips:
        return edges
    return [*edges, *((edge[::-1], -index) for edge, index in edges)]


def process_input(data):
    tiles = {}
    edges = {}
    for group in data.split("\n\n"):
        tileid, tile = group.split(":")
        tileid = int(tileid[5:])
        tile = np.genfromtxt(StringIO(tile), dtype="U1", delimiter=1, comments="S")
        tiles[tileid] = {"tile": tile, "edges": {}}
        for edgeid, index in get_edges(tile):
            edges.setdefault(edgeid, []).append(tileid)
            tiles[tileid]["edges"][edgeid] = index
    return tiles, edges


def get_corners(edges):
    counts = collections.Counter(
        (x[0] for x in filter(lambda x: len(x) == 1, edges.values()))
    )
    return map(lambda x: x[0], counts.most_common(4))


# below are functions written for part 2
def tile_to_string(tile):
    return "\n".join(map(lambda x: "".join(x), tile))


def print_tile(tile):
    print(tile_to_string(tile))


def rotate(points, k=1):
    # Rotate clockwise
    return np.rot90(points, k=k, axes=(1, 0))


def flip(points):
    return np.fliplr(points)


def perspectives(tile):
    for k, do_flip in itertools.product(range(0, 5), [False, True]):
        # rotate around up to 3 times
        new_tile = rotate(tile, k=k)
        if do_flip:
            new_tile = flip(new_tile)
        yield new_tile


def print_tile_combos(tile):
    for new_tile in perspectives(tile):
        print_tile(new_tile)
        print("-" * new_tile.shape[0])


def get_neighbors(tiles, edges, tileid):
    return set(
        (neighbor, edge)
        for edge in tiles[tileid]["edges"]
        for neighbor in edges[edge]
        if neighbor != tileid and tiles[tileid]["edges"][edge] > 0
    )


def make_top_left(tiles, edges, tileid):
    neighbors = get_neighbors(tiles, edges, tileid)
    # want the edges to be 2,3 (right/bottom)
    tile = tiles[tileid]["tile"]
    positions = sorted([tiles[tileid]["edges"][edge] for _, edge in neighbors])
    # remove as we are updating/rotating
    for edge in tiles[tileid]["edges"]:
        edges[edge].remove(tileid)
    tiles[tileid]["edges"] = {}

    if positions == [1, 2]:
        tile = rotate(tile)
    elif positions == [3, 4]:
        tile = rotate(tile, k=-1)
    elif positions == [1, 4]:
        tile = rotate(tile, k=2)

    # update again
    for edgeid, index in get_edges(tile, add_flips=False):
        if index not in [2, 3]:
            continue
        edges[edgeid].append(tileid)
        tiles[tileid]["edges"][edgeid] = index
    tiles[tileid]["tile"] = tile


# align tile based on reference tile position
def align_tile(tiles, edges, ref_position, tileid, ref_edge):
    assert ref_position > 0
    tile = tiles[tileid]["tile"]
    # remove from everything for now
    for edge in tiles[tileid]["edges"]:
        edges[edge].remove(tileid)
    tiles[tileid]["edges"] = {}

    for new_tile in perspectives(tile):
        new_edges = dict(get_edges(new_tile, add_flips=False))
        if ref_edge not in new_edges:
            continue
        cur_position = new_edges[ref_edge]
        if abs(ref_position - cur_position) == 2:
            break

    # update again
    for edgeid, index in new_edges.items():
        edges[edgeid].append(tileid)
        tiles[tileid]["edges"][edgeid] = index
    tiles[tileid]["tile"] = new_tile


def stack_image(tiles, image, with_edges=True):
    if with_edges:
        return np.vstack(
            [np.hstack([tiles[tileid]["tile"] for tileid in row]) for row in image]
        )
    return np.vstack(
        [
            np.hstack([tiles[tileid]["tile"][1:-1, 1:-1] for tileid in row])
            for row in image
        ]
    )


def build_image(tiles, edges):
    size = int(np.sqrt(len(tiles)))
    corners = list(get_corners(edges))

    image = np.zeros((size, size), dtype=int)
    image[0, 0] = corners[0]
    make_top_left(tiles, edges, image[0, 0])

    for row in range(size):
        for col in range(size):
            for neighborid, edge in get_neighbors(tiles, edges, image[row, col]):
                position = tiles[image[row, col]]["edges"][edge]
                if neighborid in image:
                    continue
                align_tile(tiles, edges, position, neighborid, edge)
                if position == 2:
                    image[row, col + 1] = neighborid
                elif position == 3:
                    image[row + 1, col] = neighborid

    return stack_image(tiles, image, with_edges=False)


MONSTER = [
    r"..................#.",
    r"#....##....##....###",
    r".#..#..#..#..#..#...",
]
MONSTER_REGEX = [re.compile(i) for i in MONSTER]
MONSTER_HASH = "".join(MONSTER).count("#")


def count_monsters(imageref):
    for image in perspectives(imageref):
        monsters = 0
        for i in range(imageref.shape[0] - len(MONSTER)):
            for j in range(imageref.shape[1] - len(MONSTER[0])):
                subset = image[i : i + len(MONSTER), j : j + len(MONSTER[0])]
                monsters += all(
                    re.fullmatch(regex, "".join(line))
                    for line, regex in zip(subset, MONSTER_REGEX)
                )
        if monsters:
            return monsters


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input(
        """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""
    )
    test_tiles, test_edges = test_vals
    assert functools.reduce(operator.mul, get_corners(test_edges)) == 20899048083289

    puz = Puzzle(2020, 20)

    data = process_input(puz.input_data)
    tiles, edges = data

    puz.answer_a = functools.reduce(operator.mul, get_corners(edges))
    print(f"Part 1: {puz.answer_a}")

    test_image = build_image(test_tiles, test_edges)
    test_num_monsters = count_monsters(test_image)
    assert np.sum(test_image == "#") - MONSTER_HASH * test_num_monsters == 273

    image = build_image(tiles, edges)
    num_monsters = count_monsters(image)
    puz.answer_b = np.sum(image == "#") - MONSTER_HASH * num_monsters
    print(f"Part 2: {puz.answer_b}")
