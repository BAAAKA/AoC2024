import numpy as np

with open('data/day04.txt','r') as f: 
    lines = f.read().splitlines()

def get_cell(r,c):
    if r>=0 and r<len(lines) and c>=0 and c<len(lines[0]):
        return lines[r][c]
    return '.'

def get_xmas(pos=(0,0)):
    count = 0
    for direction in np.array([(1,0),(0,1),(1,1),(1,-1)]):
        letters=""
        for i in range(0,4):
            letters += get_cell(*(pos+direction*i))
        if letters in ['XMAS', 'SAMX']:
            count+=1
    return count

def get_x_mas(pos=(0,0)):
    for direction in np.array([((1,1), (0,0), (-1,-1)),((1,-1), (0,0), (-1,1))]):
        letters=""
        for coords in direction:
            letters+=get_cell(*pos+coords)
        if letters not in ['MAS', 'SAM']:
            return 0
    return 1

totalCount = 0
totalCount2 = 0
for r in range(0,len(lines)):
    for c in range(0,len(lines[0])+1):
        totalCount += get_xmas(pos=(r,c))
        totalCount2 += get_x_mas(pos=(r,c))

print(f'Part 1: {totalCount}')
print(f'Part 2: {totalCount2}')

