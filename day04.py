import numpy as np

with open('data/day04.txt','r') as f: 
    lines = f.read().splitlines()

lines = np.array(lines)

def get_cell(r,c):
    if r>=0 and r<len(lines) and c>=0 and c<len(lines[0]):
        return lines[r][c]
    return '.'

def get_xmas(pos=(0,0)):
    count = 0
    pos = np.array(pos)
    directions = np.array([(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)])
    for direction in directions:
        letters=""
        for i in range(0,4):
            letters += get_cell(*(pos+direction*i))
        if letters == 'XMAS':
            count+=1
    return count

totalCount = 0

for r in range(0,len(lines)):
    for c in range(0,len(lines[0])+1):
        totalCount += get_xmas(pos=(r,c))

print(totalCount)
