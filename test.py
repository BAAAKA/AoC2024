import numpy as np


next_positions = [(1, np.array([2, 1])), (1, np.array([4, 3])), (1, np.array([4, 3])), (2, np.array([2, 1]))]


def summarize(next_positions):
    pos_dict = {}
    for val, pos in next_positions:
        pos_dict[tuple(pos)] = pos_dict.get(tuple(pos), 0)+val

    return [(value, np.array(key)) for key, value in pos_dict.items()]
    
    



result=summarize(next_positions)
print(result)


