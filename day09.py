from utils import read_file
import numpy as np

line = np.array(list(map(int, (read_file('data/day09.txt')[0]))))

print(line)

def gen_yield_from_behind(line):
    for index in range(0, len(line)):
        reversed_index = len(line)-index-1
        is_file = (reversed_index+1)%2

        block_id = reversed_index//2
        if is_file: 
            for i in range(line[reversed_index]):
                yield block_id, reversed_index

position = 0 # Position on the opened numberline
checksum_total = 0 
fileID = 0 # ID number based on the order of the files as they appear before reordering
index_forward = 0 # The index on the variable compressed line
index_backwards = len(line)-1
file_switch = True


generator_behind = gen_yield_from_behind(line=line)

while index_forward<index_backwards:
    # print(f'FileID {index_forward//2}, its a file: {file_switch}, position: {position}')
    # print(f'current value is {checksum_total}')
    if file_switch:
        file_length = line[index_forward]
        fileID = index_forward//2

        file_checksum = sum(range(position, position+file_length))*fileID # File checksum for the next file
        checksum_total += file_checksum

        print(f'{file_length} {file_checksum} | {checksum_total}')
        position += file_length
        index_forward += 1
    else:
        empty_length = line[index_forward]
        #print(f'> empty_length: {empty_length}')
        for i in range(empty_length):
            fileID, index_backwards = next(generator_behind)
            # print(f'> file from behind: {fileID}, calc: {position}*{fileID}')
            checksum_total += position*fileID
            position+=1
        index_forward += 1
    file_switch = file_switch == False

for i in range(10):
    fileID_runout, index_backwards_runout = next(generator_behind)
    if index_backwards_runout != index_backwards:
        break
    checksum_total += position*fileID
    position+=1



print(f'P1: {checksum_total}')


