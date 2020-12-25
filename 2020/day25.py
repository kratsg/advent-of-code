import itertools
import math

# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/


def gen_primes():
    """Generate an infinite sequence of prime numbers."""
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1


def process_input(data):
    return list(map(int, data.split("\n")))


# googling led to the baby-step giant-step algorithm
# https://www.geeksforgeeks.org/discrete-logarithm-find-integer-k-ak-congruent-modulo-b/
# and implemented https://en.wikipedia.org/wiki/Baby-step_giant-step
# Note: 20201227 (for modulo) is prime
def bsgs(base, number, modulo=20201227):
    middle = math.ceil(math.sqrt(modulo))
    # build look-up table of subject^i % modulo (for i up to sqrt(number))
    table = {pow(base, i, modulo): i for i in range(middle)}
    # base^(middle * (modulo - 2)) should equal base^(-middle) mod modulo
    factor = pow(base, modulo - middle - 1, modulo)
    # also works, why?
    # factor = pow(base, (modulo - 2) * middle, modulo)
    y = number
    for i in range(middle):
        if y in table:
            # exponent
            return i * middle + table[y]
        y = (y * factor) % modulo
        # also works, why?
        # y = (number * pow(factor, i, modulo)) % modulo

    return None


def handshake(subject, loop_size, modulo=20201227):
    return pow(subject, loop_size, modulo)


def reverse_handshake(public_keys):
    found = {}
    for prime in gen_primes():
        for public_key in public_keys:
            loop_size = bsgs(prime, public_key)
            if loop_size:
                found[public_key] = (prime, loop_size)
        if len(found) == len(public_keys):
            return found


if __name__ == "__main__":
    from aocd.models import Puzzle

    assert handshake(7, 8) == 5764801
    assert handshake(7, 11) == 17807724
    assert bsgs(7, 5764801) == 8
    assert bsgs(7, 17807724) == 11
    test_vals = process_input(
        """5764801
    17807724"""
    )
    test_found = reverse_handshake(test_vals)
    assert handshake(test_vals[1], test_found[test_vals[0]][1]) == 14897079

    puz = Puzzle(2020, 25)

    data = process_input(puz.input_data)
    found = reverse_handshake(data)
    puz.answer_a = handshake(data[1], found[data[0]][1])
    print(f"Part 1: {puz.answer_a}")

    """ No part 2!
    assert False

    puz.answer_b = None
    print(f"Part 2: {puz.answer_b}")
    """
