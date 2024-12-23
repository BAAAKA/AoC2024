import numpy as np
import math
import itertools
from collections import defaultdict
from utils import read_file
lines = [line.split('-') for line in read_file('data/day23.txt')]


network = defaultdict(set)
for n,m in lines:
    network[n].add(m)
    network[m].add(n)


combinations = set()
for key in network:
    if 't' == key[0]:
        print(f'{key}: {network[key]}')
        for n in network[key]:
            for overlap in network[n] & network[key]:
                combinations.add(tuple(sorted((key, n, overlap))))

print(combinations)
print(len(combinations))


# That's not the right answer; your answer is too high.  2351
