import numpy as np

with open('data/day01.txt','r') as f:
    lines = f.read().splitlines()

print(lines)

splitnr = np.array([list(map(int, v.split('   '))) for v in lines])

sorted_splitnr = np.sort(splitnr.T)

diffs = sum(abs(sorted_splitnr[0] - sorted_splitnr[1]))
print(f'Difference is {diffs}')

