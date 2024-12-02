with open('data/day02.txt','r') as f:
    lines = f.read().splitlines()

parsed = [list(map(int, line.split())) for line in lines]
differences = [[line[v]-line[v-1] for v in range(1, len(line))] for line in parsed]

save_lines = []

for dif in differences:
    max_dif = max(abs(min(dif)), max(dif))<=3
    no_zero = 0 not in dif
    all_same = all([v*dif[0]>0 for v in dif])
    print(dif)
    print([max_dif, no_zero, all_same])
    print(all([max_dif, no_zero, all_same]))
    if all([max_dif, no_zero, all_same]):
        save_lines.append(dif)


print(f'P1 Count save lines: {len(save_lines)}')
