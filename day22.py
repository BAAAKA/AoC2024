import numpy as np
import math
from utils import read_file
lines = list(map(int, read_file('data/day22.txt')))

def get_next_secret_nr(nr):
    nr = nr ^ (64 * nr )
    nr = nr%16777216
    nr = nr^int(nr/32)
    nr = nr%16777216
    nr = nr ^ (nr * 2048)
    nr = nr%16777216
    return nr


def get_n_sn(secret_value, n):
    for i in range(n):
        secret_value = get_next_secret_nr(secret_value)
    return secret_value

def get_last_digits(secret_value, n):
    last_digits = []
    last_digits.append(secret_value%10)
    for i in range(n):
        secret_value = get_next_secret_nr(secret_value)
        last_digits.append(secret_value%10)
    
    return last_digits

res = [get_n_sn(secret_value, 2000) for secret_value in lines]
print(f'P1: {sum(res)}')

combination_dict = {}

for secret_value in lines:
    # print(f'secret_value: {secret_value}')
    known_tuples = set()
    last_digits = get_last_digits(secret_value, 2000)
    changes = [last_digits[i+1] - last_digits[i] for i in range(len(last_digits)-1)]

    for i in range(4,len(changes)+1):
        # print(f'{changes[i-4:i]}: {last_digits[i]}')
        last4changes = tuple(changes[i-4:i])
        if last4changes in known_tuples:
            continue
        combination_dict[last4changes] = combination_dict.get(last4changes, 0) + last_digits[i]
        known_tuples.add(last4changes)


max_key = max(combination_dict, key=combination_dict.get)
print(f'P2: {max_key} {combination_dict[max_key]}') 

