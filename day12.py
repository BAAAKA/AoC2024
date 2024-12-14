from utils import read_file
import numpy as np

lines = np.array([list(row) for row in read_file('data/day12.txt')])
print(lines)

def get_cell(pos):
    if pos[0]>=0 and pos[1]>=0 and pos[0]< len(lines) and pos[1] < len(lines[0]):
        return lines[*pos]
    else:
        return '.'

lines_marking = np.full_like(lines, False, dtype=bool)
def cell_is_marked(pos, mark_it=True):
    value = lines_marking[*pos]
    if mark_it:
        lines_marking[*pos] = True
    return value

all_directions = np.array([
    [1,0],
    [-1,0],
    [0,1],
    [0,-1],
    [1,1],  
    [-1,-1],
    [-1,1],
    [1,-1],
])
def get_corner_count(current_pos, current_letter, same_letter_neighbors):
    down, up, right, left, down_right,up_left,up_right,down_left = [current_letter == get_cell(pos) for pos in current_pos+all_directions]
    inside_corners =  (not up_right and up and right)+(not up_left and up and left)+(not down_left and down and left)+(not down_right and down and right)

    count = len(same_letter_neighbors)
    if count == 0:
        outside_corners = 4
    elif count == 1:
        outside_corners = 2
    elif count > 2:
        outside_corners = 0
    elif count == 2:
        pos1 = same_letter_neighbors[0]
        pos2 = same_letter_neighbors[1]
        if pos1[0] == pos2[0] or pos1[1] == pos2[1]:
            outside_corners = 0
        else:
            outside_corners = 1
    return outside_corners+inside_corners


directions = np.array([
    [1,0],
    [-1,0],
    [0,1],
    [0,-1],
])
def get_all_neighbors(current_pos, current_letter):
    same_letter_neighbors = [tuple(pos.tolist()) for pos in current_pos+directions if get_cell(pos)==current_letter]
    edge_count = 4 - len(same_letter_neighbors)
    corner_count = get_corner_count(current_pos, current_letter, same_letter_neighbors)
    valid_neighbors = [neighbor for neighbor in same_letter_neighbors if not cell_is_marked(neighbor, mark_it=True)]
    return valid_neighbors, edge_count, corner_count

def get_next_positions(current_positions, current_letter):
    edge_count_total = 0
    corner_count_total = 0
    next_positions = set()
    for current_pos in current_positions:
        valid_neighbors, edge_count, corner_count = get_all_neighbors(current_pos=current_pos, current_letter=current_letter)
        edge_count_total += edge_count
        corner_count_total += corner_count
        next_positions.update(valid_neighbors)

    return next_positions, edge_count_total, corner_count_total


field_results = []

for r in range(len(lines)):
    for c in range(len(lines[0])):
        if cell_is_marked((r, c), mark_it=False):
            continue

        total_edges = 0
        total_fields = 1 # 1 instead of 0 since starting positon
        total_corners = 0

        current_positions = [(r,c)]
        current_letter=lines[*current_positions[0]]
        cell_is_marked(current_positions[0]) # mark current starting pos

        while len(current_positions)>0:
            current_positions, edge_count, corner_count = get_next_positions(current_positions=current_positions, current_letter=current_letter)
            # print(f'the next pos: {current_positions}')
            total_edges += edge_count
            total_corners += corner_count
            total_fields += len(current_positions)

        print(f'{current_letter}: total_edges: {total_edges} | total_fields: {total_fields} | total_corners: {total_corners}')
        field_results.append((str(current_letter), total_edges, total_fields, total_corners))

print(f'Results: {field_results}')
print(f'P1: {sum(e*a for l, e, a, c in field_results)}')
print(f'P2: {sum(c*a for l, e, a, c in field_results)}')

