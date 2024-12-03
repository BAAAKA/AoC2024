import numpy as np
with open('data/day01.txt','r') as f:
    sorted_leftc, sorted_rightc = np.sort(np.array([list(map(int, v.split())) for v in f.read().splitlines()]).T, axis=1)
print(f'Part 1: Difference is {sum(abs(sorted_leftc - sorted_rightc))}')
print(f'Part 2: Similarity is {sum(v*dict(zip(*np.unique(sorted_rightc, return_counts=True))).get(v, 0) for v in sorted_leftc)}')


