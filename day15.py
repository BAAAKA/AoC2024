from utils import read_file
import numpy as np
import re

lines = read_file('data/day15.txt')
directions = {'<':(0, -1),'>':(0, 1),'v':(1, 0),'^':(-1, 0),} # row, col

whitespace_index = np.where(np.array(lines) == '')[0][0]

commands = ''.join(lines[whitespace_index+1:])
store_map = np.array([list(row) for row in lines[:whitespace_index]])
wide_store = []

wider_version = {"#" :'##', 'O': '[]', '.': '..', '@': '@.'}
for row in store_map:
    wide_store.append(list(''.join([wider_version[symbol] for symbol in row])))

store_map = np.array(wide_store)



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

def move_boxes_horizontal(store_map, curr_pos, next_empty_pos, command):
    row = curr_pos[0]
    store_map_row = store_map[row]
    indexes = [next_empty_pos[1], curr_pos[1]]
    move_idx_for_char = 0
    if command == '<':
        move_idx_for_char = 1
    left_idx = min(indexes) + move_idx_for_char
    right_idx = max(indexes) + move_idx_for_char
    if command == '<':
        return np.concatenate((store_map_row[:left_idx-1],store_map_row[left_idx:right_idx],['.'],store_map_row[right_idx:]))
    else:
        return np.concatenate((store_map_row[:left_idx],['.'],store_map_row[left_idx:right_idx],store_map_row[right_idx+1:]))

def move_boxes_vertical(store_map, curr_pos, command):
    parsed_command = directions[command]
    new_robot_pos = np.array(curr_pos)+parsed_command
    pos_set_to_check = set([tuple(curr_pos.tolist())])
    all_affected_pos = set([tuple(curr_pos.tolist())])
    # print(f'pos_set_to_check: {pos_set_to_check} | parsed_command: {parsed_command}')

    for i in range(100):
        next_pos_set_to_check = set()
        for pos in pos_set_to_check:
            new_pos = np.array(pos)+parsed_command
            symbol = store_map[*new_pos]
            # print(f'{np.array(pos)}+{parsed_command}=new_pos: {new_pos} | symbol: {symbol}')
            if symbol == '#':
                return store_map, curr_pos
            if symbol == '[': 
                neighbor = new_pos + np.array([0, 1])
                next_pos_set_to_check.add(tuple(new_pos.tolist()))
                next_pos_set_to_check.add(tuple(neighbor.tolist()))
            elif symbol == ']': 
                neighbor = new_pos + np.array([0, -1])
                next_pos_set_to_check.add(tuple(new_pos.tolist()))
                next_pos_set_to_check.add(tuple(neighbor.tolist()))
        # print(next_pos_set_to_check)
        all_affected_pos.update(next_pos_set_to_check)
        pos_set_to_check = next_pos_set_to_check
        if pos_set_to_check == set():
            # print(f'empty set, breaking with {all_affected_pos} ')
            break
    
    all_affected_pos_with_sym = []
    for pos in all_affected_pos:
        all_affected_pos_with_sym.append((pos, str(store_map[*pos])))
        store_map[*pos]='.'
    for pos, sym in all_affected_pos_with_sym:
        new_pos = np.array(pos)+parsed_command
        store_map[*new_pos] = sym
    return store_map, new_robot_pos
            



for command in commands:
    parsed_command = directions[command]
    new_pos = curr_pos+parsed_command
    symbol = store_map[*new_pos]
    # print(f'{command} | new_pos: {new_pos} | {store_map[*new_pos]}')

    if symbol == '#':
        continue
    if symbol in ['[', ']']:
        if command in ['>', '<']:
            next_empty_pos = check_behind_boxes(store_map=store_map, parsed_command=parsed_command, new_pos=new_pos)
            if isinstance(next_empty_pos, str) and next_empty_pos=='#':
                continue
            row_idx = curr_pos[0]
            store_map[row_idx] = move_boxes_horizontal(store_map, curr_pos, next_empty_pos, command)
            curr_pos = new_pos
        elif command in ['^', 'v']:
            store_map, curr_pos = move_boxes_vertical(store_map, curr_pos, command)

    else:
        store_map[*curr_pos] = '.'
        store_map[*new_pos] = '@'
        curr_pos = new_pos

    # print(store_map)

total_value = 0
for r in range(len(store_map)):
    for c in range(len(store_map[0])):
        if store_map[r][c] == '[':
            total_value += r*100+c




print(f'P1: {total_value}')

