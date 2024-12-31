import numpy as np
from utils import read_file

lines = read_file('data/day25.txt')
locks = []
keys = []
for i in range(0, len(lines), 8):
    pattern = np.array([list(l) for l in lines[i:i+7]])
    counts = np.array([np.count_nonzero(l=='#')-1 for l in pattern.T])
    if lines[i] == '#####':
        keys.append(counts)
    else:
        locks.append(counts)




def valid_combination(key, lock):
    # print(f'{key}, {lock}')
    return np.all(key+lock<=5)

total_valid = 0
for key in keys:
    for lock in locks:
        
        total_valid += valid_combination(key, lock)

print(f'total_valid: {total_valid}')