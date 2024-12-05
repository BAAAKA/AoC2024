# 8:37 start
# 8:49 p1 
# 9:02 p2

with open('data/day05.txt','r') as f: 
    lines = f.read().splitlines()

manuals = []
rules = []

for line in lines:
    if ',' in line:
        manuals.append(line)
    elif '|' in line:
        rules.append(line)

manuals = [list(map(int, man.split(','))) for man in manuals]
rules = [list(map(int, rule.split('|'))) for rule in rules]

def validiation_p1(manual):
    for before, after in rules:
        if before in manual and after in manual:
            if manual.index(before)>manual.index(after):
                return 0
    return manual[len(manual)//2]

def correction_p2(manual):
    if validiation_p1(manual) != 0:
        return 0
    
    while validiation_p1(manual) == 0:
        for before, after in rules:
            if before in manual and after in manual:
                index_before = manual.index(before)
                index_after = manual.index(after)
                if index_before>index_after:
                    val = manual.pop(index_before)
                    manual.insert(index_after,val)
    return manual[len(manual)//2]

print(f'Part 1: {sum(validiation_p1(man) for man in manuals)}')
print(f'Part 2: {sum(correction_p2(man) for man in manuals)}')
