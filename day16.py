
from utils import read_file
import numpy as np
import re
import heapq

maze = np.array([list(row) for row in read_file('data/day16.txt')])
start_pos = np.where(maze=='S')
goal_pos = np.where(maze=='E')
start_pos = np.array(list(map(int, (start_pos[0][0], start_pos[1][0]))))
goal_pos = np.array(list(map(int, (goal_pos[0][0], goal_pos[1][0]))))

directions = {'<':(0, -1),'>':(0, 1),'v':(1, 0),'^':(-1, 0)} # row, col
turning = {
    '<': ['v','^'],
    '>': ['v','^'],
    'v': ['>','<'],
    '^': ['>','<']
}

print(maze)
print(start_pos)
print(goal_pos)

closed_list = set() # 
open_list = []
all_visited_fields = set()
valid_finishers = []


def get_next_possible_moves(current_node):
    score, pos, direction, prev_node = current_node
    next_direction_nodes = [(score+1000, pos, new_d, (score, pos, direction)) for new_d in turning[direction] if closed_list_valid(score+1000, pos, new_d)]

    new_pos = tuple((np.array(pos)+directions[direction]).tolist())
    next_step = []
    if closed_list_valid(score+1, new_pos, d) and maze[*new_pos] != '#':
        next_step = [(score+1, new_pos, direction, (score, pos, d))]
    return next_step+next_direction_nodes


closed_list_dict = {}
def closed_list_valid(score, pos, direction):
    the_key = (tuple(pos),direction)
    if the_key in closed_list_dict:
        if closed_list_dict[the_key]<score: # Bad
            return False
        else:
            # dif = abs(score-closed_list_dict[the_key])
            # print(f'Overwriting possible previous path, score dif: {dif}')
            closed_list_dict[the_key] = score
            return True
    else:
        closed_list_dict[the_key] = score
        return True



start_node = (0, tuple(start_pos.tolist()), '>', None) 
heapq.heappush(open_list, start_node)


for i in range(10000000):
    current_node = heapq.heappop(open_list)
    # print(f'current_node: {current_node}')
    all_visited_fields.add(current_node)
    _, pos, d, prev_node = current_node

    if maze[*pos] == 'E':
        print(f'{i} Found E: {current_node}')
        break


    next_possible_moves = get_next_possible_moves(current_node)
    for move in next_possible_moves:
        heapq.heappush(open_list, move)
    
    # print(f'open_list: {open_list}')


(11047, (2, 15), '^', (11046, (3, 15), '^'))

history_dict = {}

for score, pos, d, p in all_visited_fields:
    # if (score, pos, d) in history_dict:
    #     print(f'{(score, pos, d)} has 2 valid prev: {history_dict[(score, pos, d)]} and {p}')
    history_dict[(score, pos, d)] = history_dict.get((score, pos, d), []) + [p]



def rec_fill(p):
    if not p:
        return None
    score, pos, d = p 
    maze[*pos] = 'O'
    for next_p in history_dict[p]:
        rec_fill(next_p)

score, pos, d, p = current_node
rec_fill(p)
    


# #  (11042, (7, 15), '^'): (10042, (7, 15), '^'), 
print(maze)   
print(f'P1: {score}')   
total_seats = np.count_nonzero(maze=='O')+1
print(f'P2: {total_seats}')

