
import numpy as np
import copy
from utils import read_file
lines = read_file('data/day18.txt')

byte_c = [list(map(int, l.split(','))) for l in lines]
# print(byte_c)
left, right = np.array(byte_c).T
map_size = (int(max(left)), int(max(right)))
all_positions = set([(0,0)])
the_map = np.full(np.array(map_size) + (1,1), '.')
the_map[0,0] = 'O'
the_map[*map_size] = 'G'


def get_cell(the_map, pos):
    if pos[0]>=0 and pos[1]>=0 and pos[0]< len(the_map) and pos[1] < len(the_map[0]):
        return the_map[*pos]
    else:
        return '#'

def get_valid_surrounding(the_map, position):
    directions = ((0, -1),(0, 1),(1, 0),(-1, 0))
    np_pos = np.array(position)
    return set(list((tuple((np_pos+direction).tolist()) for direction in directions if get_cell(the_map, np_pos+direction) in ['.', 'G'])))

def get_next_steps(the_map, positions):
    all_next_steps = set()
    for position in positions:
        next_steps = get_valid_surrounding(the_map, position)
        # print(f'next_steps: {next_steps}')
        all_next_steps.update(next_steps)
    return all_next_steps

def get_steps_till_goal(the_map, all_positions, byte_c, bytes_falling = 12):

    for b in byte_c[:bytes_falling]:
        the_map[*b] = '#'

    for i in range(1000):
        for pos in all_positions:
            if the_map[*pos] == 'G':
                # print(the_map)
                # print(f'P1: {i}')
                return i
            the_map[*pos] = 'O'
        all_positions = get_next_steps(the_map=the_map, positions=all_positions)
        # print(f'all_positions: {all_positions}')
    return False

def find_value(mini=1000, maxi=3450):
    return int((mini+maxi)/2)



mini = 0
maxi = len(byte_c)

for i in range(1000):
    if abs(maxi-mini)<2:
        print(f'{i} {guess} found nr {maxi}: {byte_c[maxi-1]}')

        break

    guess = find_value(mini, maxi)
    steps = get_steps_till_goal(copy.deepcopy(the_map), all_positions, byte_c, guess)

    if steps>0:
        print(f'{i} {guess} found exist after {steps}')
        mini = guess
    else:
        print(f'{i} {guess} found NO EXIST {steps}')
        maxi = guess
    
    
    




