from operator import add, mul
import sys

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
    pointer = memory[i]
    if doPrint:
      print('  ', '[{}]'.format(i), pointer, memory)
    if pointer == 99: break
    elif pointer in OPS:
      left_addr  = memory[i+1]
      right_addr = memory[i+2]
      dest_addr  = memory[i+3]
      left_val  = memory[left_addr]
      right_val = memory[right_addr]
      dest_val  = memory[dest_addr]
      memory[dest_addr] = OPS[pointer](left_val, right_val)
      if doPrint:
        print('    ', 'LEFT ', '[{}]'.format(left_addr), left_val)
        print('    ', 'RIGHT', '[{}]'.format(right_addr), right_val)
        print('    ', 'DEST ', '[{}]'.format(dest_addr), dest_val, '->', memory[dest_addr])
      [next(iterable) for x in range(3)] # move forwards 4
    else:
      RuntimeError('Cannot parse program')

  return memory2program(memory)

assert computer('1,0,0,0,99') == '2,0,0,0,99'
assert computer('2,3,0,3,99') == '2,3,0,6,99'
assert computer('2,4,4,5,99,0') == '2,4,4,5,99,9801'
assert computer('1,1,1,4,99,5,6,0,99') == '30,1,1,4,2,5,6,0,99'
assert computer('1,9,10,3,2,3,11,0,99,30,40,50') == '3500,9,10,70,2,3,11,0,99,30,40,50'

def modify_program(program, noun=12, verb=2):
  temp = program2memory(program)
  temp[1] = noun
  temp[2] = verb
  return memory2program(temp)


program = open('input/day-02.txt').read()
# To do this, before running the program, replace position 1 with the value 12 and replace position 2 with the value 2.
print(computer(modify_program(program)))

for noun in range(100):
  for verb in range(100):
    result = computer(modify_program(program, noun=noun, verb=verb))
    memory = program2memory(result)
    if memory[0] == 19690720:
      print('noun={} verb={}'.format(noun, verb))
      sys.exit(0)
