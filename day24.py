import numpy as np
from utils import read_file
import copy
import random

lines = read_file('data/day24.txt')
empty_index = lines.index('')

operations = [[k1, k2, operation, result_key] for k1, operation, k2, _, result_key in (line.split(' ') for line in lines[empty_index+1:])]
v_dict = {k[:-1]:int(v) for k, v in (line.split(' ') for line in lines[:empty_index])}


def get_result(_v_dict, k1, k2, operation):
    val_k1 = int(_v_dict[k1])
    val_k2 = int(_v_dict[k2])
    if operation == 'AND':
        if val_k1 == val_k2 == 1:
            return 1
    elif operation == 'OR':
        if val_k1 == 1 or val_k2 == 1:
            return 1
    elif operation == 'XOR':
        if val_k1 != val_k2:
            return 1
    return 0

def array_to_binary(_v_dict, array_keys):
    binary_result = ''.join([str(_v_dict[key]) for key in sorted(array_keys, reverse=True)])
    return binary_result

def perform_operations(_v_dict, _operations):
    while len(_operations) > 0:
        change_occured = False
        for i, (k1, k2, operation, result_key) in enumerate(_operations):
            if k1 in _v_dict and k2 in _v_dict:
                _v_dict[result_key] = get_result(_v_dict, k1, k2, operation)
                # print(f'setting {result_key} as {_v_dict[result_key]} as {k1} ({_v_dict[k1]}) {k2} ({_v_dict[k2]}) {operation}')
                _operations.pop(i)
                change_occured = True
                break
        if not change_occured:
            # print(_operations)
            # print("Infinite Loop")
            return _v_dict
            return False

    return _v_dict

def adjust_operations(operations, gene):
    new_operations = copy.deepcopy(operations)
    for i1, i2 in gene:
        new_operations[i1][3], new_operations[i2][3] = new_operations[i2][3], new_operations[i1][3]
    return new_operations

def get_wrong_z_values(binary_result, z_wires):
    incorrect_z_values = []
    str_result = str(binary_result)
    str_z_wire = str(z_wires).ljust(len(str_result),'0')
    for i in range(len(str_result)):
        idx = len(str_result)-i-1
        if str_result[i] != str_z_wire[i]:
            incorrect_z_values.append('z'+f'{idx}'.zfill(2))
    return incorrect_z_values


def get_loss(v1, v2, _operations):
    expected_result = v1 + v2
    # print(f'{v1}+{v2}={expected_result}')
    binary_result = str(bin(expected_result)[2:])
    min_length = len(binary_result)
    binary_v1 = str(bin(v1)[2:]).zfill(min_length)
    binary_v2 = str(bin(v2)[2:]).zfill(min_length)

    manual_v_dict = {}
    manual_v_dict.update({'x'+f'{i}'.zfill(2):digit for i, digit in enumerate(binary_v1[::-1])})
    manual_v_dict.update({'y'+f'{i}'.zfill(2):digit for i, digit in enumerate(binary_v2[::-1])})


    x_wires = array_to_binary(manual_v_dict, [key for key in manual_v_dict if key[0] == 'x'])
    y_wires = array_to_binary(manual_v_dict, [key for key in manual_v_dict if key[0] == 'y'])

    res_dict = perform_operations(copy.deepcopy(manual_v_dict), copy.deepcopy(_operations))
    if res_dict == False:
        # print('Infinite Loop')
        return 9999
        # raise Exception('Infinite Loop')
    z_wires = array_to_binary(res_dict, [key for key in res_dict if key[0] == 'z'])

    int_nr_len = len(str(int(binary_result, 2)))
    bin_nr_len = len(str(binary_result))
    # print('x:'+f'{int(x_wires, 2)}'.zfill(int_nr_len)+' | '+f'{x_wires}'.zfill(bin_nr_len))
    # print('y:'+f'{int(y_wires, 2)}'.zfill(int_nr_len)+' | '+f'{y_wires}'.zfill(bin_nr_len))
    # print('e:'+f'{int(binary_result, 2)}'+f' | {binary_result}')
    # print('z:'+f'{int(z_wires, 2)}'.zfill(int_nr_len)+f' | '+f'{z_wires}'.zfill(bin_nr_len))


    # print(f'Incorrect z values: {get_wrong_z_values(binary_result, z_wires)}')

    if int(x_wires, 2) != v1:
        raise Exception(f'x values {int(x_wires, 2)} {v1} are different')
    if int(y_wires, 2) != v2:
        raise Exception(f'y values {int(y_wires, 2)} {v2} are different')

    loss = bin(int(binary_result, 2) ^ int(z_wires, 2)).count('1')
    # print(f'loss: {loss}')
    return loss

def get_random_gene(max_value = 221):
    while True:
        gene = tuple((random.randint(1, max_value), random.randint(1, max_value)) for _ in range(1))
        if len(set((v for t in gene for v in t))) == len(gene)*2:
            return gene

def mutate_gene(gene, max_value=221):
    if random.random() < 0.5:
        pair_to_mutate = random.choice(gene)
        mutated_pair = (random.randint(1, max_value), random.randint(1, max_value))
        
        gene = tuple(mutated_pair if pair == pair_to_mutate else pair for pair in gene)
    return gene

def combine_genes(gene1, gene2):
    gene1_pairs = random.sample(gene1, 2)
    gene2_pairs = random.sample(gene2, 2)
    
    combined_gene = gene1_pairs + gene2_pairs
    combined_gene = mutate_gene(combined_gene, max_value=221)

    flattened_gene = [v for pair in combined_gene for v in pair]
    if len(set(flattened_gene)) == len(flattened_gene):
        # print('returning valid gene')
        return combined_gene
        
    # print('Gene is invalid, returning random gene')
    return get_random_gene()

random.seed(35) 
min_value = 2**44
max_value = 2**45
numbers = [(random.randint(min_value, max_value - 1), random.randint(min_value, max_value - 1)) for i in range(5)]

total_population = 100
chosen_population = 5
chosen_parents = 0
new_children = 0
population = [get_random_gene() for i in range(total_population)]

for generation in range(10000):
    next_gen = []
    for gene in population:
        adjusted_operations = adjust_operations(operations=operations, gene=gene)

        total_loss = 0
        for v1, v2 in numbers:
            loss = get_loss(v1, v2, adjusted_operations)
            total_loss += loss
        next_gen.append((total_loss, gene))
    next_gen = sorted(next_gen, key=lambda x: x[0])
    best_loss = next_gen[0][0]
    # print(f'next_gen: {next_gen[:chosen_population]}')
    selected_population = [next_gen[i][1] for i in range(chosen_population)]
    for i in range(new_children):
        gene1, gene2 = random.sample(selected_population[chosen_parents:], 2)
        combined_gene = combine_genes(gene1, gene2)
        # print(f'{gene1} {gene2} = {combined_gene}')
        selected_population.append(combined_gene)

    population = [get_random_gene() for i in range(total_population-len(selected_population))] + selected_population
    sorted_population = [tuple(sorted(tup)) for tup in population]
    population = set(sorted_population)
    print(f'GENERATION {generation} best_loss: {best_loss} | {next_gen[0][1]}')


v1, v2 = numbers[1]
# v1, v2 = 12,13
loss = get_loss(v1, v2, operations)
print(loss)

# fgt,fpq,nqk,pcp,srn,z07,z24,z32


# # wrong_z_val = ['z'+f'{i}'.zfill(2) for i in range(len(z_wires)) if z_wires[i] != expected_binary[i]]
# # print(f'wrong_z_val: {wrong_z_val}')

# operations = [[k1, k2, operation, result_key] for k1, operation, k2, _, result_key in (line.split(' ') for line in lines[empty_index+1:])]

# op_by_resultkey = {result_key: (k1, k2, operation, result_key) for k1, k2, operation, result_key in operations}

# dependencies_array = {}
# def get_operation(res_key):
#     if res_key not in op_by_resultkey:
#         return []

#     k1, k2, operation, result_key = op_by_resultkey[res_key]
#     result = [(k1, k2, operation, result_key)]
#     result += get_operation(k1)
#     result += get_operation(k2) 
#     return result

# def get_all_z_to(nr):
#     return set(['z'+f'{i}'.zfill(2) for i in range(nr)])

# def get_expected_keys(nr):
#     expected_keys = set()
#     expected_keys.update(['x'+f'{i}'.zfill(2) for i in range(nr+1)])
#     expected_keys.update(['y'+f'{i}'.zfill(2) for i in range(nr+1)])
#     return expected_keys

# for i in range(len(z_wires)):
#     z_name = 'z'+f'{i}'.zfill(2)
#     related_keys = set()
#     all_operations = get_operation(z_name)
#     related_keys.update(list((k1 for k1, k2, operation, result_key in all_operations if k1[0] in ['y', 'x'])))
#     related_keys.update(list((k2 for k1, k2, operation, result_key in all_operations if k2[0] in ['y', 'x'])))
#     correct_keys = get_expected_keys(i)
#     too_many = related_keys-correct_keys
#     missing = correct_keys-related_keys

#     if len(too_many) + len(missing) != 0:
#         print(f'{z_name} ---')
#         print(f'Keys Too Many: {too_many}')
#         print(f'Missing Keys: {missing}')



