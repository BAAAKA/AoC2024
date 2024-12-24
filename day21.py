import numpy as np
from utils import read_file

lines = read_file('data/day21.txt')

fpad = np.array([['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [' ', '0', 'A']])
dpad = np.array([[' ', '^', 'A'], ['<', 'v', '>']])
directions = {'<':np.array((0, -1)),'>':np.array((0, 1)),'v':np.array((1, 0)),'^':np.array((-1, 0)),} # row, col

fpad_dict = {(row, col): str(fpad[row, col]) for row in range(fpad.shape[0]) for col in range(fpad.shape[1])}
fpad_v_to_coord_dict = {str(fpad[row, col]): (row, col) for row in range(fpad.shape[0]) for col in range(fpad.shape[1])}

dpad_dict = {(row, col): str(dpad[row, col]) for row in range(dpad.shape[0]) for col in range(dpad.shape[1])}
dpad_v_to_coord_dict = {str(dpad[row, col]): (row, col) for row in range(dpad.shape[0]) for col in range(dpad.shape[1])}

current_symbol_dict = ['A','A','A','A']
pad_type = ['fpad', 'dpad', 'dpad', 'dpad']
def adj_position(pad_index, direction):
    global current_symbol_dict
    global pad_type
    cur_pad_type = pad_type[pad_index]
    cur_symbol = current_symbol_dict[pad_index]
    if cur_pad_type == 'dpad':
        cur_pos = dpad_v_to_coord_dict[cur_symbol]
        new_pos = tuple(cur_pos + directions[direction])
        new_sym = dpad_dict[new_pos]
    elif cur_pad_type == 'fpad':
        cur_pos = fpad_v_to_coord_dict[cur_symbol]
        new_pos = tuple(cur_pos + directions[direction])
        new_sym = fpad_dict[new_pos]
    print(f'Switched {cur_symbol} to {new_sym}')
    current_symbol_dict[pad_index] = new_sym



def get_direction(pad_index, cgoal_sym):
    global current_symbol_dict
    global pad_type
    pad_type = pad_type[pad_index]
    cur_sym = current_symbol_dict[pad_index]

    if pad_type == 'dpad':
        coord_dict = dpad_v_to_coord_dict
    elif pad_type == 'fpad':
        coord_dict = fpad_v_to_coord_dict

    empty_pad_row, empty_pad_col = coord_dict[' ']
    cpos = coord_dict[cur_sym]
    goal = coord_dict[cgoal_sym]

    possible_moves = set()
    crow, ccol = cpos
    grow, gcol = goal

    loss = abs(grow-crow)+abs(ccol-gcol)
    
    if loss == 0:
        return [('A', 0)]
    if ccol>gcol:
        possible_moves.add('<')
    if ccol<gcol:
        possible_moves.add('>')
    if grow>crow:
        possible_moves.add('v')
    if grow<crow:
        possible_moves.add('^')

    if len(possible_moves) == 2:
        if empty_pad_row == crow:
            possible_moves = possible_moves - {'<', '>'}
        elif empty_pad_col == ccol:
            possible_moves = possible_moves - {'^', 'v'}

    return [(d, loss) for d in possible_moves]



pad_index = 0
csym = current_symbol_dict[pad_index]
cgoal_sym = '7'

possible_moves = get_direction(pad_index, cgoal_sym)
print(f'possible_moves fpad {possible_moves}')

if pad_type == 'dpad':
    coord_dict = dpad_v_to_coord_dict
elif pad_type == 'fpad':
    coord_dict = fpad_v_to_coord_dict

all_possible_moves = []
for next_move_symbol, loss in possible_moves:
    cpos = coord_dict[csym] # 
    cgoal = coord_dict[next_move_symbol]
    empty_pad = coord_dict[' ']

    possible_moves = get_direction(pad_index, cgoal_sym) # CHECK THIS
    all_possible_moves = all_possible_moves + possible_moves

min_val = min(t[1] for t in all_possible_moves)
all_possible_moves = [t for t in all_possible_moves if t[1] == min_val]
print(all_possible_moves)

# possible_moves = get_next_step(possible_moves, dpad_v_to_coord_dict, current_symbol_dict[1])
# print(possible_moves)
# possible_moves = get_next_step(possible_moves, dpad_v_to_coord_dict, current_symbol_dict[2])
# print(possible_moves)
# possible_moves = get_next_step(possible_moves, dpad_v_to_coord_dict, current_symbol_dict[3])
# print(possible_moves)





