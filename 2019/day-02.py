from operator import add, mul

OPS = {1: add,
       2: mul}

def program2memory(program):
  return list(map(int, program.split(',')))

def memory2program(memory):
  return ','.join(map(str, memory))

def computer(program, doPrint=False):
  global OPS
  memory = program2memory(program)
  iterable = iter(range(len(memory)))
  if doPrint:
    print('START', program)
    print('  ', 'MEMORY', memory)

  for i in iterable:
    token = memory[i]
    if doPrint:
      print('  ', '[{}]'.format(i), token, memory)
    if token == 99: break
    elif token in OPS:
      left_idx  = memory[i+1]
      right_idx = memory[i+2]
      dest_idx  = memory[i+3]
      left_val  = memory[left_idx]
      right_val = memory[right_idx]
      dest_val  = memory[dest_idx]
      memory[dest_idx] = OPS[token](left_val, right_val)
      if doPrint:
        print('    ', 'LEFT ', '[{}]'.format(left_idx), left_val)
        print('    ', 'RIGHT', '[{}]'.format(right_idx), right_val)
        print('    ', 'DEST ', '[{}]'.format(dest_idx), dest_val, '->', memory[dest_idx])
      [next(iterable) for x in range(3)] # move forwards 4
    else:
      RuntimeError('Cannot parse program')

  return memory2program(memory)

assert computer('1,0,0,0,99') == '2,0,0,0,99'
assert computer('2,3,0,3,99') == '2,3,0,6,99'
assert computer('2,4,4,5,99,0') == '2,4,4,5,99,9801'
assert computer('1,1,1,4,99,5,6,0,99') == '30,1,1,4,2,5,6,0,99'
assert computer('1,9,10,3,2,3,11,0,99,30,40,50') == '3500,9,10,70,2,3,11,0,99,30,40,50'
