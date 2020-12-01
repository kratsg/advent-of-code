# Advent of code Year 2020 Day 1 solution
# Author = Giordon Stark
# Date = December 2020

import itertools
import math
with open((__file__.rstrip("code.py")+"input.txt"), 'r') as input_file:
    input = input_file.read()
    input = list(map(int, input.split()))
    doublets = itertools.combinations(input, 2)
    triplets = itertools.combinations(input, 3)

for doublet in doublets:
    if sum(doublet) == 2020:
        break

print(f"Part One : {math.prod(doublet)}")

for triplet in triplets:
    if sum(triplet) == 2020:
        break

print(f"Part Two : {math.prod(triplet)}")
