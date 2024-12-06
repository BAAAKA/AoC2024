import numpy as np
from copy import deepcopy

with open('data/day06.txt','r') as f: 
    original_lines = np.array([list(row) for row in f.read().splitlines()])
    lines = deepcopy(original_lines)

def get_start():
    for i in range(len(lines)):
        if '^' in lines[i]:
            return np.array((i, np.argwhere(lines[i]=='^')[0][0]))

start_position = get_start()


def next_direction():
    while True:
        for i in range(0,4):
            yield i

def get_cell(r,c):
    if r>=0 and r<len(lines) and c>=0 and c<len(lines[0]):
        return lines[r][c]
    return '0'


def get_walked_map():
    get_next_direction = next_direction()
    current_direction = next(get_next_direction)
    current_position = start_position
    next_index = current_position + directions[current_direction]

    for i in range(6000):
        next_index = current_position + directions[current_direction]
        value = get_cell(*next_index)
        
        if value == '#':
            current_direction = next(get_next_direction)
        elif value in ['.', 'X']:
            lines[tuple(current_position)] = 'X'
            current_position = next_index

        if value == '0':
            lines[tuple(current_position)] = 'X'
            return lines
    return None

directions = np.array([(-1,0),(0,1),(1,0),(0,-1)])

finished_map = get_walked_map()
print(finished_map)
print(f'P1: {np.count_nonzero(finished_map =='X')}')

possible_obsticles = np.argwhere(finished_map == 'X')

print(possible_obsticles)

stuck_positions = 0
for pos_obs in possible_obsticles:
    if all(pos_obs == start_position):
        continue

    lines = deepcopy(original_lines)
    lines[tuple(pos_obs)] = '#'
    result = get_walked_map()
    if result is None:
        print(f'Found a stuck one with pos {pos_obs}')
        stuck_positions+=1

print(f'P2: {stuck_positions}')













