from utils import read_file
import numpy as np

line = np.array(list(map(int, (read_file('data/day09.txt')[0]))))


files = line[::2]
empty = line[1::2]
id_numbers = np.array(list(range(len(files))))

print(id_numbers)
print(files)
print(empty)
fline = np.array([])
for i in range(len(line)):
    is_file = (i+1)%2
    block = i//2
    if is_file:
        fline = np.append(fline, [str(block)]*line[i], axis=None)
    else:
        fline = np.append(fline, ['.']*line[i], axis=None)

# def index_last_nondot(fline):
#     for i in range(len(fline)):
#         if fline[::-1][i] != '.':
#             return len(fline)-i-1

# def get_value(fline):
#     return sum((int(v)*i for i, v in enumerate(fline) if v != '.'))

# for i in range(20000000):

#     if fline[i] == '.':
#         last_index = index_last_nondot(fline)
#         fline[i] = fline[last_index]
#         fline[last_index] = '.'

#     if len(set(fline[i+1:]))==1:
#         print('break')
#         break

# print(f'P1: {get_value(fline)}')