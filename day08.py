from utils import read_file
import numpy as np
import itertools

lines = read_file('data/day08.txt')
symbols = set(''.join(lines)) - set('.')
lines = np.array([list(row) for row in lines])
lines_ant = np.full(lines.shape, '.', dtype='<U1')
coords = {}

for symbol in symbols:
    coords[symbol] = np.array(tuple(zip(*np.where(lines==symbol))))

def get_antinode(pos1, pos2):
    dif = pos1 - pos2
    return pos1+dif, pos2-dif

def get_antinode_harmonics(pos1, pos2):
    dif = pos1 - pos2
    repetitions = int(len(lines)/max(abs(dif))+1)
    return [pos1+dif*modifier for modifier in range(-repetitions, repetitions)]

def set_cell(pos):
    if pos[0]>=0 and pos[1]>=0 and pos[0]< len(lines) and pos[1] < len(lines[0]):
        lines_ant[pos[0]][pos[1]] = '#'

for symbol in coords:
    combinations = list(itertools.combinations(coords[symbol], 2))
    for pos1, pos2 in combinations:
        # antinode_positions = get_antinode(pos1, pos2) # Part 1
        antinode_positions = get_antinode_harmonics(pos1, pos2) # Part 2
        [set_cell(pos) for pos in antinode_positions]
        
print(lines_ant)
print(f'P1/P2: {np.count_nonzero(lines_ant == '#')}')
