from utils import read_file
import numpy as np
import re

lines = read_file('data/day14.txt')
robots = [list(map(int, re.findall(r'-?\d+', line))) for line in lines]
print(f'robots: {robots}')
map_rows, map_cols = 103, 101

def move_robot(robot):
    # print(robot)
    pos_h, pos_v, h_move, v_move = robot

    # print(f'Before: v{pos_v} | h{pos_h}')
    pos_h = (pos_h+h_move)%map_cols
    pos_v = (pos_v+v_move)%map_rows

    # print(f'After: v{pos_v} | h{pos_h}')
    return pos_h, pos_v, h_move, v_move 


def get_pos_dict(robots):
    pos_dict = {}
    for robot in robots:
        pos_h, pos_v, h_move, v_move = robot
        pos_dict[(pos_h, pos_v)] = 1+pos_dict.get((pos_h, pos_v), 0)
    return pos_dict

def visualize(robots, only_print_tree=True):
    pos_dict = get_pos_dict(robots)
    if only_print_tree and not max(pos_dict.values())==1:
        return None
    

    for r in range(map_rows):
        print(f'')
        for c in range(map_cols):
            val = str(pos_dict.get((c, r), '.'))
            print(val, end='')
    print('')
    if only_print_tree:
        input('Next:')


for i in range(100000):

    print(f'Gen {i+1}')
    robots = [move_robot(robot) for robot in robots]
    # print(robots)
    # input('Next:')
    visualize(robots)

pos_dict = get_pos_dict(robots)


map_rows, map_cols
counting = [0,0,0,0]
for position, v in pos_dict.items():
    pos_h, pos_v = position
    if pos_h==map_cols//2 or pos_v==map_rows//2:
        continue
    elif pos_h>map_cols//2 and pos_v>map_rows//2:
        index = 0
    elif  pos_h>map_cols//2 and pos_v<map_rows//2:
        index = 1
    elif  pos_h<map_cols//2 and pos_v>map_rows//2:
        index = 2
    elif  pos_h<map_cols//2 and pos_v<map_rows//2:
        index = 3
    
    counting[index] += v


print(counting)
print(f'P1: {np.prod(counting)}')

# For p2 check the terminal