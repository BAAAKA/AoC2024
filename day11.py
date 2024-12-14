from utils import read_file
import numpy as np
import time

line = list(map(int, read_file('data/day11.txt')[0].split()))
print(line)

blink_memo = {}
def blink(value):
    if value in blink_memo:
        return blink_memo[value]

    if value == 0:
        return [1]
    value_str = str(value)
    if len(value_str)%2==0:
        hlen = len(value_str)//2
        result = list(map(int, [value_str[:hlen], value_str[hlen:]]))
    else:
        result = [value*2024]
    blink_memo[value] = result
    return result

def get_new_line(line_dict):
    new_dict = {}
    for key, value in line_dict.items():
        results = blink(key)
        for result in results:
            new_dict[result] = new_dict.get(result, 0) + value
    return new_dict



start_time = time.time()

line_dict = {}
for v in line:
    line_dict[v] = 1

print(line_dict)


steps = 75
for i in range(1,steps+1):
    line_dict = get_new_line(line_dict)

print(f'Length: {len(line_dict)}') 
print(line_dict)
print(sum(line_dict[k] for k in line_dict))

"""
Length: 29115525
Total execution time: 8.843361 seconds
"""



end_time = time.time()

execution_time = end_time - start_time
print(f"Total execution time: {execution_time:.6f} seconds")

