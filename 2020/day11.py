import numpy as np

def sliding_window(data, window_size, step_size):
  for i in range(0, data.shape[0] - window_size + 1):
      for j in range(0, data.shape[1] - window_size + 1):
        yield data[i:i+window_size,j:j+window_size].reshape((-1,window_size))

def process_input(data):
    central = np.asarray(list(map(tuple, data.replace("L", "1").replace(".", "0").split())), dtype='int')
    result = np.full((central.shape[0]+2, central.shape[1]+2), 0)
    result[1:-1,1:-1] = central
    return result

def count_occupied(data):
    return np.sum(data==2)

def any_occupied(data):
    return np.any(data==2)

def tick_part1(data):
    result = []
    for window in sliding_window(data, 3, 1):
        center = window[1,1]
        occupied = count_occupied(window)
        if center == 1 and occupied == 0:
            new_center = 2
        elif center == 2 and occupied >= 5:
            new_center = 1
        else:
            new_center = center

        result.append(new_center)
    result = np.array(result).reshape((data.shape[0]-2, data.shape[1]-2))
    data[1:-1,1:-1] = result

def closest_seat(data):
    try:
        return next(i for i in data if i!=0)
    except StopIteration:
        return 0

def tick_part2(data):
    datasub = data[1:-1,1:-1]
    result = []
    for i in range(datasub.shape[0]):
        for j in range(datasub.shape[1]):
            updown = datasub[0,:]
            leftright = datasub[:,0]
            diagonal = np.diagonal(datasub)
            otherdiagonal = np.diagonal(np.fliplr(np.roll(datasub, -1, axis=1)))

            seats = [
              closest_seat(updown[1:-i]),
              closest_seat(updown[-i:][::-1]),
              closest_seat(leftright[1:-j]),
              closest_seat(leftright[-j:][::-1]),
              closest_seat(diagonal[-i:][::-1]),
              closest_seat(diagonal[1:-i]),
              closest_seat(otherdiagonal[-i:][::-1]),
              closest_seat(otherdiagonal[1:-i])]
            occupied = count_occupied(seats)
            print(i, j, seats)
            if datasub[0,0] == 1 and occupied == 0:
                new_center = 2
            elif datasub[0,0] == 2 and occupied >= 5:
                new_center = 1
            else:
                new_center = datasub[0,0]

            result.append(new_center)
            datasub = np.roll(datasub, -1, axis=1)
        datasub = np.roll(datasub, -1, axis=0)
    result = np.array(result).reshape((data.shape[0]-2, data.shape[1]-2))
    data[1:-1,1:-1] = result

def process(data, tick=tick_part1):
    prev_occupied = count_occupied(data)
    while True:
        print(prev_occupied, data)
        tick(data)
        occupied = count_occupied(data)
        if occupied == prev_occupied:
            return occupied
        prev_occupied = occupied


if __name__ == "__main__":
    from aocd.models import Puzzle

    test_vals = process_input("""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""")
    #assert process(test_vals) == 37
    puz = Puzzle(2020, 11)

    data = process_input(puz.input_data)

    #puz.answer_a = process(data)
    #print(f"Part 1: {puz.answer_a}")

    test_vals = process_input("""L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""")
    print(process(test_vals, tick=tick_part2))
    assert False

    puz.answer_b = None
    print(f"Part 2: {puz.answer_b}")
