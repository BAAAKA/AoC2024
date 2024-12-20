import numpy as np
from utils import read_file
lines = np.array([list(row) for row in read_file('data/day20.txt')])

padding_amnt = 30
lines = np.pad(lines, (padding_amnt, padding_amnt), mode='constant', constant_values='#')

start_pos = np.where(lines=='S')
goal_pos = np.where(lines=='E')
start_pos = np.array(list(map(int, (start_pos[0][0], start_pos[1][0]))))
goal_pos = np.array(list(map(int, (goal_pos[0][0], goal_pos[1][0]))))

def get_cell(the_map, pos, default_val = '#'):
    if pos[0]>=0 and pos[1]>=0 and pos[0]< len(the_map) and pos[1] < len(the_map[0]):
        return the_map[*pos]
    else:
        return default_val
    
directions = np.array([
    [1,0],
    [-1,0],
    [0,1],
    [0,-1],
])

def get_next_pos(position):
    return [(pos) for pos in position+directions if get_cell(lines, pos) in ['E', '.']]

value_map = np.zeros(lines.shape, dtype=np.int64)
position = start_pos

positions_to_check = np.empty((0, 2), dtype=np.int64)
for i in range(1,1000000):
    lines[*position] = str(i)
    value_map[*position] = i

    positions_to_check = np.append(positions_to_check, [position], axis=0)
    positions = get_next_pos(position)
    if len(positions) == 0:
        break
    position = positions[0]


def get_manhattan_map(size = 5):
    center = (size // 2, size // 2)
    manhattan_map = np.zeros((size, size), dtype=int)
    for i in range(size):
        for j in range(size):
            manhattan_map[i, j] = abs(i - center[0]) + abs(j - center[1])
    manhattan_map[manhattan_map>size//2] = 99999
    return manhattan_map

cheat_directions = np.array([
    [2,0],
    [-2,0],
    [0,2],
    [0,-2],
])

def get_slice(position, size=5):
    side_len = size // 2
    sh, eh = position[0]-side_len, position[0]+side_len+1
    sw, ew = position[1]-side_len, position[1]+side_len+1
    return value_map[sh:eh, sw:ew]
    

def get_next_pos_cheat(position):
    return [(pos) for pos in position+cheat_directions if get_cell(value_map, pos, default_val=0) != 0]


def get_cheat_values_per_pos(pos, size = 21):
    value_map_slice = get_slice(pos, size)
    value_at_pos = int(value_map[*pos])
    walk_map = get_manhattan_map(size)
    flattened = (value_map_slice-value_at_pos-walk_map).flatten()
    positive_values = flattened[flattened>0]
    return positive_values

cheat_count = {}
for pos in positions_to_check:
    # print(f'Checking {pos}')
    positive_values = get_cheat_values_per_pos(pos, size = 41)
    for val in positive_values:
        cheat_count[int(val)] = cheat_count.get(int(val), 0) + 1

total_above = 0
cheat_count = {key: cheat_count[key] for key in sorted(cheat_count)}
for k in cheat_count:
    if k>=100:
        total_above += cheat_count[k]

print(f'P2: {total_above}')
