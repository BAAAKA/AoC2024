def array_to_binary(_v_dict, array_keys):
    binary_result = ''.join([str(_v_dict[key]) for key in sorted(array_keys)])
    return binary_result

v1 = 10
binary_v1 = str(bin(v1)[2:])
print(f':{binary_v1}')
manual_v_dict = {}
for i in range(len(binary_v1)):
    manual_v_dict['x'+f'{i}'.zfill(2)] = binary_v1[i]

x_wires = array_to_binary(manual_v_dict, [key for key in manual_v_dict if key[0] == 'x'])
y_wires = array_to_binary(manual_v_dict, [key for key in manual_v_dict if key[0] == 'y'])


print('x: '+f'{int(x_wires, 2)}'.zfill(2)+f' | {x_wires}')