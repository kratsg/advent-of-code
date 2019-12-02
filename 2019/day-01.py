import numpy as np
module_masses = np.genfromtxt('input/day-01.txt')

def module_fuel(module_mass):
  fuel = np.floor_divide(module_mass, 3) - 2
  return fuel.clip(min=0)

assert module_fuel(12) == 2
assert module_fuel(14) == 2
assert module_fuel(1969) == 654
assert module_fuel(100756) == 33583

modules_fuel = module_fuel(module_masses)
print(np.sum(modules_fuel))

def recursive_module_fuel(module_mass):
  total_fuel = 0
  mass = module_mass
  while mass > 0:
    fuel = module_fuel(mass)
    total_fuel += fuel
    mass = fuel
  return total_fuel

assert recursive_module_fuel(100756) == 50346

print(np.sum([recursive_module_fuel(m) for m in module_masses]))
