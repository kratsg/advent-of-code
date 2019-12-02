import numpy as np
module_masses = np.genfromtxt('input/day-01.txt')

def module_fuel(module_mass):
  return np.floor_divide(module_mass, 3) - 2

modules_fuel = module_fuel(module_masses)
print(np.sum(modules_fuel))
