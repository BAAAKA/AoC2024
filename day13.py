from utils import read_file
import numpy as np
import re

lines = read_file('data/day13.txt')
tara = []
crane_games = []
for line in lines:
    if line == '':
        crane_games.append(tara)
        tara = []
    else:
        tara.append(list(map(int, re.findall(r'\d+', line))))
crane_games.append(tara)

def get_total_cost(crane_games, part2_mod = True):
    all_solutions = []
    total_cost = 0
    for crane_game in crane_games:
        arm1 = crane_game[0]
        arm2 = crane_game[1]
        target = crane_game[2] 

        if part2_mod:
            target = target + np.array([10000000000000, 10000000000000])

        values = np.array([
            arm1, arm2
        ])
        xy = np.linalg.solve(values.T, target)
        cost = sum(xy*[3,1])
        all_solutions.append([xy, cost, round(cost)])
        if abs(round(cost) - cost)>0.001:
            continue # Solution is invalid

        total_cost+=round(cost)
    return total_cost

print(f'P1: {get_total_cost(crane_games, part2_mod=False)}')
print(f'P2: {get_total_cost(crane_games, part2_mod=True)}')
