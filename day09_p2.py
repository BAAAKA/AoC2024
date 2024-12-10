from utils import read_file
import numpy as np

line = np.array(list(map(int, (read_file('data/day09.txt')[0]))))
print(line)

empty_pos = np.cumsum(line)[:-1:2] # ?
empty_len = line[1::2]
empties = np.vstack((empty_pos, empty_len)).T
print(empties)

def get_pos(empties, target_value):
    if empties.size == 0 or max(empties[:, 1]) < value:
        return 'None Found'
    for index, empty_space in enumerate(empties[:, 1]):
        if target_value<=empty_space:
            return index

position = sum(line)
total = 0
for i, value in enumerate(reversed(line)):
    index = len(line) - i - 1 # The index forward
    is_file = (index+1)%2
    # print(f'{index} file len:{value} | is_file: {is_file} | position: {position}')
    empties = empties[empties[:, 0] < position]

    if not is_file:
        position-=value
        continue

    result = get_pos(empties, value)
    file_id = index//2
    if result is 'None Found':
        # print(f'None found for {str(file_id)*value}')
        checksum = sum(range(position-value, position))*file_id
        total += checksum
        # print(f'Checksum: {checksum}')
    else:
        # print(f'Found for {str(file_id)*value}')
        empty_position, length = empties[result]
        if length == value:
            # print(f'delete: {empties[result]}')
            empties = np.delete(empties, result, axis=0)
        else: 
            empties[result][1] = length-value
            empties[result][0] = empty_position+value
            # print(f'adjusted: {empties[result]}')
        
        
        checksum = sum(range(empty_position, empty_position+value))*file_id
        total += checksum
        # print(f'Checksum: {checksum}, empty_position: {empty_position} | {list(range(empty_position, empty_position+value))}')
    position-=value

print(f'Total: {total}')

# 6421724645083