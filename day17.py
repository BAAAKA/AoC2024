
from utils import read_file
lines = read_file('data/day17.txt')

nr_to_register = {
    4: 'A',
    5: 'B',
    6: 'C',
}

def get_combo_value(value, register):
    if value <= 3:
        return value
    if value in [4,5,6]:
        return register[nr_to_register[value]]
    if value == 7:
        print('Invalid nr 7')
        return None

def instrucitons(opcode, value, register):
    if opcode == 0:
        # The adv instruction (opcode 0) performs division. 
        # The numerator is the value in the A register. The denominator is found by raising 2 to the 
        # power of the instruction's combo operand. (So, an operand of 2 would divide A by 4 (2^2); 
        # an operand of 5 would divide A by 2^B.) The result of the division operation is truncated to 
        # an integer and then written to the A register.
        register['A'] = int(register['A']/2**get_combo_value(value, register))
        # print(f'0: Set A to {register['A'] }')
    elif opcode == 1:
        # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's 
        # literal operand, then stores the result in register B.
        register['B'] = value ^ register['B']
        # print(f'1: Set B to {register['B']}') 
    elif opcode == 2: 
        # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 
        # (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        register['B'] = get_combo_value(value, register)%8
        # print(f'2 Setting register B to {register['B'] }')
    elif opcode == 3:
        # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, 
        # it jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, 
        # the instruction pointer is not increased by 2 after this instruction.
        if register['A'] == 0:
            # print('3 Do nothing')
            pass
        else:
            # print(f'3 Jump to {value} and dont increase the value by 2 next time')
            return (3, 0)
    elif opcode == 4:
        # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result 
        # in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        register['B'] = register['B'] ^ register['C']
        # print(f'4 Set B to {register['B']}')

    elif opcode == 5:
        # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. 
        # (If a program outputs multiple values, they are separated by commas.)
        # print(f'5 output value {get_combo_value(value, register)%8}')
        return (5, get_combo_value(value, register)%8)
    elif opcode == 6:
        # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the 
        # B register. (The numerator is still read from the A register.)
        register['B'] = int(register['A']/2**get_combo_value(value, register))
        # print(f'6: Set B to {register['B'] }')
    elif opcode == 7:
        # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is 
        # stored in the C register. (The numerator is still read from the A register.)
        register['C'] = int(register['A']/2**get_combo_value(value, register))
        # print(f'7: Set C to {register['C'] }')
    return (2, 0)

def get_output(register, instruction_values):
    idx = 0
    output_values = []
    for i in range(10000):
        if idx >= len(instruction_values):
            # print('idx too large')
            break
        opcode = instruction_values[idx]
        value = instruction_values[idx+1]
        result, returnvalue = instrucitons(opcode=opcode, value=value, register=register)
        # print(f'Got result {result}')
        if result == 2:
            idx += 2
        elif result == 3:
            idx = value
        elif result == 5:
            idx += 2
            output_values.append(returnvalue)

    # print(register)
    return output_values


def adjust_digit(i):
    return (i-1)*3

def get_last_digit_thats_different(ara1, ara2):
    for i in range(len(ara1) - 1, -1, -1):
        if ara1[i] != ara2[i]:
            return i

read_register = {nr_to_register[i+4]:int(v) for i, v in enumerate([lines[0][12:], lines[1][12:], lines[2][12:]])}
instruction_values = [int(v) for v in lines[4][9:].split(',')]


print(f'read_register: {read_register}')
print(f'instruction_values: {instruction_values}')
target_values = ','.join(list(map(str, instruction_values)))


modara = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(1000):
    # print(f'Checking A: {a_value}')
    a_value = int(2**adjust_digit(len(instruction_values)) + sum((2**adjust_digit(i)*v for i, v in enumerate(modara))))

    modified_resgister = {'A':a_value,'B':read_register['B'],'C':read_register['C'],}
    output_values = get_output(modified_resgister, instruction_values)
    print(f'{i}: value {a_value}')
    print(f'{output_values}')
    print(f'{instruction_values}')
    if ','.join(list(map(str, output_values))) == target_values:
        print(f'Found match at {a_value}')
        break   
    idx_last_digit = get_last_digit_thats_different(instruction_values, output_values)+1
    modara[idx_last_digit] += 1
    print(modara)





