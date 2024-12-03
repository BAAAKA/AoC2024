import re

def counter(match_val, state={"enabled": True}):
    if match_val=='don\'t()':
        state['enabled'] = False
    elif match_val=='do()':
        state['enabled'] = True
    elif state['enabled']:
        n, m = list(map(int, match_val[4:-1].split(',')))
        return n*m
    return 0

with open('data/day03.txt','r') as f: 
    line = "_".join(f.read().splitlines())

matches = re.findall("mul\(\d*,\d*\)", line)
total = sum(counter(match) for match in matches)
print(f'Part 1: {total}')

matches = re.findall("mul\(\d*,\d*\)|do(?:n't)?\(\)", line)
total = sum(counter(match) for match in matches)
print(f'Part 2: {total}')

