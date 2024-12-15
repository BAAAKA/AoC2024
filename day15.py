from utils import read_file
import numpy as np
import re

lines = read_file('data/day15.txt')
directions = {'<':(0, -1),'>':(0, 1),'v':(1, 0),'^':(-1, 0),} # row, col

whitespace_index = np.where(np.array(lines) == '')[0][0]

commands = ''.join(lines[whitespace_index+1:])
store_map = np.array([list(row) for row in lines[:whitespace_index]])
# wide_store = np.array([])
# for row in store_map:
#     print(row)
    

coords = np.where(store_map=='@')
curr_pos = np.array(list(map(int, (coords[0][0], coords[1][0]))))

print(store_map)
print(commands)
print(curr_pos)

def check_behind_boxes(store_map, parsed_command, new_pos):
    for i in range(100):
        new_pos = new_pos+parsed_command
        symbol = store_map[*new_pos]
        if symbol == '#':
            return '#'
        if symbol == '.':
            return new_pos


for command in commands:
    parsed_command = directions[command]
    new_pos = curr_pos+parsed_command
    symbol = store_map[*new_pos]
    # print(f'{command} | new_pos: {new_pos} | {store_map[*new_pos]}')

    if symbol == '#':
        continue
    if symbol == 'O':
        next_empty_pos = check_behind_boxes(store_map=store_map, parsed_command=parsed_command, new_pos=new_pos)
        if isinstance(next_empty_pos, str) and next_empty_pos=='#':
            continue
        store_map[*next_empty_pos] = 'O'
        store_map[*curr_pos] = '.'
        store_map[*new_pos] = '@'
        curr_pos = new_pos
    else:
        store_map[*curr_pos] = '.'
        store_map[*new_pos] = '@'
        curr_pos = new_pos

    # print(store_map)

total_value = 0
for r in range(len(store_map)):
    for c in range(len(store_map[0])):
        if store_map[r][c] == 'O':
            total_value += r*100+c




print(f'P1: {total_value}')

