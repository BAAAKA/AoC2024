import numpy as np
from utils import read_file
import random as rn
import time
import heapq
import math

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

def apply_direction(direction, _pad_symbols):
    if direction == 'A' and all(v=='A' for v in _pad_symbols[:-1]):
        return True, _pad_symbols, _pad_symbols[-1]

    for i in range(len(pad_type_array)):
        pad_type = pad_type_array[i]
        pad_symbol = _pad_symbols[i]
        if direction == 'A':
            direction = pad_symbol
            continue

        new_position_is_valid, new_symbol = get_new_symbol(pad_type=pad_type, symbol=pad_symbol, direction=direction)
        if not new_position_is_valid:
            return False, _pad_symbols, None
        new_pad_symbols = _pad_symbols[:i] + (new_symbol, ) + _pad_symbols[i+1:]
        return True, new_pad_symbols, None # Valid, new array, final pad pressed button





def get_shortest_history(remaining_code):
    heap = []
    pad_symbols = ('A',) * len(pad_type_array)
    visited_set = set()
    press_history = ()
    loss = 0
    heapq.heappush(heap, (loss, len(press_history), pad_symbols, press_history, remaining_code))
    shortest_code_so_far = len(remaining_code)

    while heap:
        # time.sleep(1)
        # print(heap)
        loss, history_len, _pad_symbols, press_history, remaining_code  = heapq.heappop(heap)
        if len(remaining_code)>shortest_code_so_far:
            continue
        if (_pad_symbols, remaining_code) in visited_set:
            continue
        else:
            visited_set.add((_pad_symbols, remaining_code))

        # print(f"history_len {history_len}, _pad_symbols {_pad_symbols}, press_history {press_history}")
        for direction in ['<','>','v','^','A']:
            valid, new_pad_symbols, final_pad_value = apply_direction(direction=direction, _pad_symbols=_pad_symbols)
            # print(f'valid: {valid} | direction: {direction} | pad_symbols: {_pad_symbols} | new_pad_symbols: {new_pad_symbols} | final_pad_value: {final_pad_value}')
            if not valid:
                continue

            new_loss = calculate_loss_all_pads(new_pad_symbols, remaining_code)
            total_loss = new_loss+history_len*history_mod+len(remaining_code)*remaining_code_mod
            if final_pad_value:
                # print(f'Pressed {final_pad_value} with row {new_pad_symbols}')
                if final_pad_value == remaining_code[0]:
                    if len(remaining_code)==1:
                        # print(f'Pressed {final_pad_value} | press_history: {press_history}') 
                        press_history = press_history + (direction, )
                        return press_history
                    else:
                        heapq.heappush(heap, (total_loss, history_len+1, new_pad_symbols, press_history + (direction, ), remaining_code[1:]))
                        if len(remaining_code[1:])<shortest_code_so_far:
                            shortest_code_so_far = len(remaining_code[1:])
            else:
                heapq.heappush(heap, (total_loss, history_len+1, new_pad_symbols, press_history + (direction, ), remaining_code))

def calculate_loss(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

A_position = dpad_v_to_coord_dict['A']
def calculate_loss_all_pads(_pad_symbols, remaining_code):
    target_positions = (A_position, )*(len(pad_type_array)-1) + (fpad_v_to_coord_dict[remaining_code[0]],)
    current_position = tuple(dpad_v_to_coord_dict[symbol] for symbol in _pad_symbols[:-1]) + (fpad_v_to_coord_dict[_pad_symbols[-1]],)

    n_values = len(target_positions)
    losses = (calculate_loss(target_positions[i], current_position[i])*(i+1) for i in range(n_values))
    weights = [i**2 for i in range(n_values)]
    weighted_sum = sum(l * w for l, w in zip(losses, weights))
    weight_sum = sum(weights)
    loss = weighted_sum / weight_sum
    return int(loss)

# Elapsed time: 1.6638903617858887 seconds no loss
# Elapsed time: 1.4850494861602783 seconds
pad_type_array = ['dpad']*5 + ['fpad']
history_mod = 1
remaining_code_mod= 1

start_time = time.time()
all_histories = []
for code in target_codes:
    print(f'Code: {code}')
    best_history = get_shortest_history(code)
    all_histories.append((code, best_history))

end_time = time.time()

total_value = 0
for code, best_history in all_histories:
    number = int(''.join(char for char in code if char.isdigit()))
    print(f'{len(best_history)} {number}={number*len(best_history)} {''.join(best_history)}')
    total_value += number*len(best_history)

print(f'Total {total_value}')

elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
