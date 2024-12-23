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


def get_comb(network):
    combinations = set()
    for key in network:
        for n in network[key]:
            for overlap in network[n] & network[key]:
                combinations.add(tuple(sorted((key, n, overlap))))
    return combinations

def is_in_all(current_lan, new_pc):
    for pc in current_lan:
        if new_pc not in network[pc]:
            return False
    return True


def get_larger_lan(current_lans):
    combinations = set()
    for current_lan in current_lans:
        pc_candidates = network[current_lan[0]]
        new_bigger_lan = [tuple(sorted(list(current_lan)+[pc_cand])) for pc_cand in pc_candidates if is_in_all(current_lan, pc_cand)]
        combinations.update(new_bigger_lan)
    return combinations

current_lans = [tuple([pc]) for pc in network.keys()]
for i in range(20   ):
    if len(current_lans)<20:
        print(f'{i}, {len(current_lans)}: {current_lans}')
    else:
        print(f'{i}, {len(current_lans)}')

    current_lans = get_larger_lan(current_lans)
    if len(current_lans)==1:
        result = current_lans.pop()
        print(f'P2: {','.join(result)}')
        break




# print(combinations)
# print(len(combinations))

