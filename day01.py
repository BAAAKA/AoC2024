import numpy as np

with open('data/day01.txt','r') as f:
    lines = f.read().splitlines()


leftc, rightc = np.array([list(map(int, v.split('   '))) for v in lines]).T

sorted_leftc = np.sort(leftc)
sorted_rightc = np.sort(rightc)

diffs = sum(abs(sorted_leftc - sorted_rightc))
print(f'P1: Difference is {diffs}')

unique, counts = np.unique(rightc, return_counts = True)
right_dict = dict(zip(map(int, unique), map(int, counts)))
total = sum([v*right_dict.get(v, 0) for v in leftc])

print(f'P2: Sym is {total}')
