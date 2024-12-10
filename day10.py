from utils import read_file
import numpy as np

lines_str = read_file('data/day10.txt')
print('\n'.join(lines_str))
lines = np.array([list(map(int, row)) for row in lines_str])

def get_cell(pos):
    if pos[0]>=0 and pos[1]>=0 and pos[0]< len(lines) and pos[1] < len(lines[0]):
        return int(lines[*pos])
    else:
        return '.'
    

def summarize(next_positions):
    pos_dict = {}
    for val, pos in next_positions:
        pos_dict[tuple(pos)] = pos_dict.get(tuple(pos), 0)+val

    return [(value, np.array(key)) for key, value in pos_dict.items()]

directions = np.array([
    [1,0],
    [-1,0],
    [0,1],
    [0,-1],
])

start_positions = []
for row in range(0, len(lines)):
    for col in range(0, len(lines[0])):
        if get_cell((row, col))==0:
            start_positions.append((row,col))

total_score = 0
total_rating = 0
for start_pos in start_positions:
    start_pos = np.array(start_pos)
    positions = [(1, start_pos)]
    current_value = get_cell(start_pos)
    for i in range(0,10):
        next_positions=[]
        for paths_to_here, position in positions:
            next_positions += [(paths_to_here, pos) for pos in position+directions if get_cell(pos)==current_value+1]


        positions = summarize(next_positions)


        current_value+=1
        if current_value==9:
            score = len(positions)
            rating = sum(paths_to_here for paths_to_here, pos in positions)
            # print(f'FINISHED score: {score} |rating: {rating}')
            total_score += score
            total_rating += rating
            break


print(f"P1: {total_score}")
print(f"P2: {total_rating}")



