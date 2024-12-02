with open('data/day02.txt','r') as f: lines = [list(map(int, l.split())) for l in f.read().splitlines()]
is_safe=lambda l: eval("all([max(abs(min(%s)), max(%s))<=3, all([v*%s[0]>0 for v in %s])])"%(([l[v]-l[v-1] for v in range(1, len(l))],)*4))
print(f'P1: {len([l for l in lines if is_safe(l)])}, P2: {len([l for l in lines if any(var for var in [l]+[l[:i]+l[i+1:] for i in range(0, len(l))] if is_safe(var))])}')


