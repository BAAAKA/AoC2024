import numpy as np
from utils import read_file
import random as rn
import time
import heapq
import math
import itertools

target_codes = read_file('data/day21.txt')

fpad = np.array([['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [' ', '0', 'A']])
dpad = np.array([[' ', '^', 'A'], ['<', 'v', '>']])
directions = {'<':np.array((0, -1)),'>':np.array((0, 1)),'v':np.array((1, 0)),'^':np.array((-1, 0)),} # row, col

fpad_dict = {(row, col): str(fpad[row, col]) for row in range(fpad.shape[0]) for col in range(fpad.shape[1])}
fpad_v_to_coord_dict = {str(fpad[row, col]): (row, col) for row in range(fpad.shape[0]) for col in range(fpad.shape[1])}

dpad_dict = {(row, col): str(dpad[row, col]) for row in range(dpad.shape[0]) for col in range(dpad.shape[1])}
dpad_v_to_coord_dict = {str(dpad[row, col]): (row, col) for row in range(dpad.shape[0]) for col in range(dpad.shape[1])}

def get_new_position(position, direction):
    return tuple((position + directions[direction]).tolist())

def calculate_distance(symbol1, symbol2, pad_type):
    if pad_type == 'dpad':
            symbol_to_pos_dict = dpad_v_to_coord_dict
    elif pad_type == 'fpad':
            symbol_to_pos_dict = fpad_v_to_coord_dict
    pos1 = symbol_to_pos_dict[symbol1]
    pos2 = symbol_to_pos_dict[symbol2]
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def get_pad_info(pad_type):
    if pad_type == 'dpad':
        symbol_to_pos_dict = dpad_v_to_coord_dict
        pos_to_symbol_dict = dpad_dict
        width = 3
        height = 2
    elif pad_type == 'fpad':
        symbol_to_pos_dict = fpad_v_to_coord_dict
        pos_to_symbol_dict = fpad_dict
        width = 3
        height = 4
    return symbol_to_pos_dict, pos_to_symbol_dict, width, height

def get_new_symbol(pad_type, symbol, direction):
    symbol_to_pos_dict, pos_to_symbol_dict, width, height = get_pad_info(pad_type)
    new_symbol = ''
    new_position_is_valid = True

    position = symbol_to_pos_dict[symbol]
    new_pos = get_new_position(position, direction)
    new_height, new_width = new_pos
    if new_height<0 or new_width<0 or new_width>width-1 or new_height>height-1:
        # print(f'{new_pos} is out of bounds!')
        new_position_is_valid = False
        return new_position_is_valid, new_symbol
    elif new_pos == symbol_to_pos_dict[' ']:
        # print('On top of the empty space!')
        new_position_is_valid = False
        return new_position_is_valid, new_symbol
    
    new_symbol = pos_to_symbol_dict[new_pos]
    return new_position_is_valid, new_symbol

def get_path(symbol, end_goal, history, max_length):
    if len(history) == max_length:
        if end_goal==symbol:
            return [history]
        else:
            return None
    
    all_histories = []
    for direction in ['<','>','v','^']:
        new_position_is_valid, new_symbol = get_new_symbol(pad_type, symbol, direction)
        if new_position_is_valid:
            result_history = get_path(new_symbol, end_goal, history+direction, max_length)
            if isinstance(result_history, list):
                all_histories += result_history
    return all_histories


pad_type = 'fpad'
paths_graph = {}

for start in fpad.flatten().tolist():
    for end in fpad.flatten().tolist():
        if ' ' in [start, end]:
            continue
        else:
            max_length = calculate_distance(start, end, pad_type)
            all_histories = get_path(symbol=start, end_goal=end, history='', max_length=max_length)
            paths_graph[(start,end)] = all_histories


pad_type = 'dpad'
for start in dpad.flatten().tolist():
    for end in dpad.flatten().tolist():
        if ' ' in [start, end]:
            continue
        else:
            max_length = calculate_distance(start, end, pad_type)
            all_histories = get_path(symbol=start, end_goal=end, history='', max_length=max_length)
            paths_graph[(start,end)] = all_histories


def get_path_dpad(start, end):
    if start == end:
        return ['A']
    return [path+'A' for path in paths_graph[(start, end)] ]

def path_to_next_path(path):
    path = 'A'+path
    parts = []
    for i in range(1, len(path)):
        start, end = path[i-1], path[i]
        result = get_path_dpad(start, end)
        parts.append(result)
    return parts 
    

memory = {}

def get_next_seq(sequence, depth):
    if (depth, sequence) in memory:
        return memory[(depth, sequence)]
        # print(f'YES')
        pass
    # all_shortest_parts = []
    total_minimum_value = 0
    if depth == 0:
        return len(sequence)
    # print(f'sequence: {sequence}')
    next_parts = path_to_next_path(sequence)
    # print(f'next_parts: {next_parts}')
    for part in next_parts:
        sequences = [get_next_seq(next_sequence, depth-1) for next_sequence in part]
        min_value = min(sequences)
        # print(f'for {sequence}: {min_value}')
        total_minimum_value += min_value
        # print(f'shortest_str: {shortest_str}')
        # all_shortest_parts.append(''.join(shortest_str))
        # print(f'part: {part} | {shortest_str}')
    # print(f'all_shortest_parts 1d: {all_shortest_parts}')
    # joined_shortest_path = ''.join(all_shortest_parts)
    memory[depth, sequence] = total_minimum_value
    return total_minimum_value



starting_position = 'A'
sequence = '980A'

total_value = 0

for code in target_codes:
    number = int(''.join(char for char in code if char.isdigit()))
    value = get_next_seq(code, 1+25)
    print(f'resuilt value: {value} = {number*value}')

    total_value += number*value

print(f'Total {total_value}')