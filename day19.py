
import numpy as np
from utils import read_file
lines = read_file('data/day19.txt')

split_idx = lines.index('')
towels = lines[:split_idx][0].split(', ')
patterns = lines[1+split_idx:]

# print(towels)
# print(patterns)
len_longest_pattern = len(max(patterns, key=len))


def get_valid_towels_from_behind(pattern):
    return [(pattern[:-len(towel)], towel) for towel in towels if pattern[-len(towel):] == towel]

def get_combinations(pattern):
    towel_dict = {}

    for i in range(len(pattern)):
        sub_pattern = pattern[:i+1]

        valid_towels = get_valid_towels_from_behind(sub_pattern)
        for req_pat, towel in get_valid_towels_from_behind(sub_pattern):
            if req_pat == '':
                towel_dict[sub_pattern] = towel_dict.get(sub_pattern, 0) + 1
            elif req_pat in towel_dict:
                towel_dict[sub_pattern] = towel_dict.get(sub_pattern, 0) + towel_dict[req_pat]

        # print(f'{sub_pattern}: {towel_dict} { valid_towels}')
    return towel_dict.get(pattern, 0)

results = []
for pattern in patterns:
    # print(f'pattern: {pattern}')
    result = get_combinations(pattern)
    results.append(result)

print(f'P1: {np.sum(np.array(results) > 0)}')
print(f'P2: {sum(results)}')





