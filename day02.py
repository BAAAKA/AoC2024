def is_safe(line):
    dif = [line[v]-line[v-1] for v in range(1, len(line))]
    max_dif = max(abs(min(dif)), max(dif))<=3
    no_zero = 0 not in dif
    all_same = all([v*dif[0]>0 for v in dif])
    return all([max_dif, no_zero, all_same])

def safe_with_removing(line):
    if is_safe(line): return True
    all_combinations = [line[:i]+line[i+1:] for i in range(0, len(line))]
    return any(comb for comb in all_combinations if is_safe(comb))

with open('data/day02.txt','r') as f:
    lines = f.read().splitlines()

parsed = [list(map(int, line.split())) for line in lines]

save_lines = [line for line in parsed if is_safe(line)]
print(f'P1 Count save lines: {len(save_lines)}')

save_lines = [line for line in parsed if safe_with_removing(line)]
print(f'P2 Count save lines: {len(save_lines)}')


