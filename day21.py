import numpy as np
from utils import read_file
import random as rn

lines = read_file('data/day21.txt')

fpad = np.array([['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [' ', '0', 'A']])
dpad = np.array([[' ', '^', 'A'], ['<', 'v', '>']])

directions = {'<':np.array((0, -1)),'>':np.array((0, 1)),'v':np.array((1, 0)),'^':np.array((-1, 0)),} # row, col

fpad_dict = {(row, col): str(fpad[row, col]) for row in range(fpad.shape[0]) for col in range(fpad.shape[1])}
fpad_v_to_coord_dict = {str(fpad[row, col]): (row, col) for row in range(fpad.shape[0]) for col in range(fpad.shape[1])}

dpad_dict = {(row, col): str(dpad[row, col]) for row in range(dpad.shape[0]) for col in range(dpad.shape[1])}
dpad_v_to_coord_dict = {str(dpad[row, col]): (row, col) for row in range(dpad.shape[0]) for col in range(dpad.shape[1])}

def calculate_loss(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def get_new_position(position, direction):
    return tuple((position + directions[direction]).tolist())


def get_valid_directions(start, end, empty_position):
    possible_moves = set() # 0 is height, 1 is width
    if start[0]>end[0] and get_new_position(start, '^') != empty_position:
        possible_moves.add('^')
    if start[0]<end[0] and get_new_position(start, 'v') != empty_position:
        possible_moves.add('v')
    if start[1]>end[1] and get_new_position(start, '<') != empty_position:
        possible_moves.add('<')
    if start[1]<end[1] and get_new_position(start, '>') != empty_position:
        possible_moves.add('>')
    
    # if len(possible_moves) == 2:
    #     if empty_position[0] == start[0]:
    #         possible_moves = possible_moves - {'<', '>'}
    #     elif empty_position[1] == start[1]:
    #         possible_moves = possible_moves - {'v', '^'}

    return possible_moves

class Pad:
    def __init__(self, pad_type, start_position):
        self.pad_type = pad_type
        self.symbol = start_position
        if pad_type == 'dpad':
            self.symbol_to_pos_dict = dpad_v_to_coord_dict
            self.pos_to_symbol_dict = dpad_dict
            self.width = 3
            self.height = 4
            self.pad_ara = dpad
        elif pad_type == 'fpad':
            self.symbol_to_pos_dict = fpad_v_to_coord_dict
            self.pos_to_symbol_dict = fpad_dict
            self.width = 3
            self.height = 2
            self.pad_ara = fpad
        else:
            print(f'UNKNOWN PAD TYPE {pad_type}')

    def get_symbol(self):
        return self.symbol

    def get_position(self):
        return self.symbol_to_pos_dict[self.get_symbol()]
    
    def print_pad(self):
        for r in range(len(self.pad_ara)):
            for c in range(len(self.pad_ara[0])):
                if (r,c) == self.get_position():
                    print("\033[1;30;43m" + self.pad_ara[r][c] + "\033[0m", end=' ')
                else:
                    print(self.pad_ara[r][c], end=' ')
            print('')

    def move(self, direction):
        new_pos = get_new_position(self.get_position(), direction)
        new_height, new_width = new_pos
        if new_height<0 or new_width<0 or new_width-1>self.width or new_height-1>self.height:
            print(f'{new_pos} is out of bounds!')
            return False
        if new_pos == self.symbol_to_pos_dict[' ']:
            print('On top of the empty space!')
            return False
        self.symbol = self.pos_to_symbol_dict[new_pos]
        return True

    def path_to_symbol(self, target_symbol):
        pos_target = self.symbol_to_pos_dict[target_symbol]
        loss = calculate_loss(pos_target, self.get_position())
        
        if target_symbol==self.get_symbol():
            return {'A'} # On top of the target
        
        return get_valid_directions(start=self.get_position(), end=pos_target, empty_position = self.symbol_to_pos_dict[' '])
    
    def __str__(self):
        return f'{self.pad_type} {self.get_symbol()} {self.get_position()}'

    def __repr__(self):
        return self.__str__()

def get_moves(code):
    pad_type_array = ['fpad'] + ['dpad']*25
    pads_array = []
    for pad_type in pad_type_array:
        the_pad = Pad(pad_type, 'A')
        pads_array.append(the_pad)

    button_index = 0
    first_pad_inputs = []
    for step in range(1000000):
        targets = [code[button_index]]
        for i in range(len(pads_array)):
            possible_targets = pads_array[i].path_to_symbol(targets[-1])
            # if len(possible_targets)>1:
            #     print(f'possible_targets: {possible_targets}')
            # target = possible_targets.pop()
            target = rn.choice(list(possible_targets))
            targets.append(target)
        
        # print('-----')
        # for pad in pads_array:
        #     pad.print_pad()
        #     print('-----')

        if all(v=='A' for v in targets[1:]):
            # print(f'Button {targets[0]} has been pressed')
            button_index+=1
            if button_index == len(code):
                first_pad_inputs.append(target[-1])
                # print('FINISHED')
                return first_pad_inputs
            

        for i in range(len(pads_array), 0, -1):
            if targets[i] != 'A':
                # print(f'{step} {[pad.get_symbol() for pad in pads_array]} {targets} pad {i} will be moved {targets[i]}')
                pads_array[i-1].move(targets[i])
                break
        
        first_pad_inputs.append(target[-1])

    


input_values = []
print(lines)
for line in lines:
    print(f'Line: {line}')
    best_solution = (99999999,'')

    for i in range(1):
        first_pad_inputs = get_moves(line)
        if len(first_pad_inputs)<best_solution[0]:
            best_solution=(len(first_pad_inputs), first_pad_inputs)

    input_values.append(best_solution)
    
total = 0
for i, (length, result) in enumerate(input_values) :
    number = int(''.join(char for char in lines[i] if char.isdigit()))
    print(f'{length} {lines[i]} {number} '+''.join(result))
    total += length*number

print(f'Total is : {total}')

# That's not the right answer; your answer is too high. 208196 202648