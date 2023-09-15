from utils import read_input, read_test

x = read_input(6)

def fn_1(x):
    x = x[0]
    for i in range(len(x)):
        if len(x[i:i+4]) == len(set(x[i:i+4])):
            return i+4
        
print(fn_1(x))


def fn_2(x):
    x = x[0]
    for i in range(len(x)):
        if len(x[i:i+14]) == len(set(x[i:i+14])):
            return i+14
        
print(fn_2(x))