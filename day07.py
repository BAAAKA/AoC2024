from utils import read_file

lines = read_file('data/day07.txt')

calibrations = []
for line in lines:
    test_val, nrs = line.split(':')
    test_val = int(test_val)
    nrs = list(map(int, nrs.split()))
    calibrations.append((test_val, nrs))

def calculate(nrs, current_value, step, test_val, enabled_pipe_operation = False):
    if current_value == test_val:
        return True
    if step == len(nrs):
        return False

    next_val = nrs[step]

    operations = [
        current_value + next_val,
        current_value * next_val,
    ]
    if enabled_pipe_operation:# Enable for Part 2
        operations.append(
            int(str(current_value) + str(next_val)), 
        )   

    return any(calculate(nrs, new_value, step+1, test_val, enabled_pipe_operation) for new_value in operations)


print(f'P1: {sum(test_val for test_val, nrs in calibrations if any(calculate(nrs, value, 1, test_val) for value in nrs))}')
print(f'P2: {sum(test_val for test_val, nrs in calibrations if any(calculate(nrs, value, 1, test_val, True) for value in nrs))}')


