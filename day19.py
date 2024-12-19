
import numpy as np
from utils import read_file
lines = read_file('data/day19.txt')

split_idx = lines.index('')
towels = lines[:split_idx][0].split(', ')
patterns = lines[1+split_idx:]

print(towels)
print(patterns)

def get_valid_towerls(pattern):
    return [towel for towel in towels if pattern[:len(towel)] == towel]


def search_combinations(pattern):
    print(f'pattern: {pattern}')
    if len(pattern) == 0:
        print('Reached the end!')
        return []
    
    valid_towels = get_valid_towerls(pattern)
    print(f'Valid Towels: {valid_towels}')
    if len(valid_towels) == 0:
        print('There were no valid combinations')
        return None

    for valid_towel in valid_towels:
        towel_len = len(valid_towel)
        result = search_combinations(pattern[towel_len:])
        if isinstance(result, list):
            result.append(valid_towel)
            return result

results = []
for pattern in patterns:
    result = search_combinations(pattern=pattern)
    if result:
        results.append(','.join(result[::-1]))
        
print(results)
print(f'P1: {len(results)}')  

