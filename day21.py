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

def calculate_loss(pos1, pos2):
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

def get_new_position(position, direction):
    return tuple((position + directions[direction]).tolist())


def get_valid_directions(start, end, empty_position):
    possible_moves = set()
    if start[0]>end[0] and get_new_position(start, '^') != empty_position:
        possible_moves.add('^')
    if start[0]<end[0] and get_new_position(start, 'v') != empty_position:
        possible_moves.add('v')
    if start[1]>end[1] and get_new_position(start, '<') != empty_position:
        possible_moves.add('<')
    if start[1]<end[1] and get_new_position(start, '>') != empty_position:
        possible_moves.add('>')
    
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
        elif pad_type == 'fpad':
            self.symbol_to_pos_dict = fpad_v_to_coord_dict
            self.pos_to_symbol_dict = fpad_dict
            self.width = 3
            self.height = 2
        else:
            print(f'UNKNOWN PAD TYPE {pad_type}')

    def get_symbol(self):
        return self.symbol

    def get_position(self):
        return self.symbol_to_pos_dict[self.get_symbol()]
    
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


pad_type_array = ['fpad', 'dpad', 'dpad']
pads_array = []
for pad_type in pad_type_array:
    the_pad = Pad(pad_type, 'A')
    pads_array.append(the_pad)

fpad = Pad('fpad', 'A')

for step in range(25):
    targets = ['0']
    for i in range(len(pads_array)):
        target = pads_array[i].path_to_symbol(targets[-1]).pop()
        targets.append(target)
        if targets[-1] == 'A': # ADJUST THIS, WHEN A BEING PRESSED, ITERATE BACK TO THE FIRST PAD AND AT EACH STEP CHECK IF ITS ALSO A, IF YES -> CONTINUE, IF NO, JUST DO THE STEP AND END
            print(f'{[pad.get_symbol() for pad in pads_array]} {targets} Pressing {targets[-1]} on the {i} pad, which leads to.. Pressing {targets[-2]} on the {i-1} pad')
            pads_array[i-1].move(targets[-2])
            break

        if i == 2:
            print(f'{[pad.get_symbol() for pad in pads_array]} {targets} Last pad {i}, pressing {targets[-1]}')
            pads_array[i].move(targets[-1])




