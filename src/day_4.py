from utils import read_input, read_test

x = read_input(4)
x_ = read_test(4)

def pre(x):
    out = []
    for y in x:
        l, r = y.split(',')
        out.append((*sorted(map(int, l.split('-'))), *sorted(map(int, r.split('-')))))
    return out


def in_1(a, b, c, d):
    if a <= c <= d <= b:
        return True
    if c <= a <= b <= d:
        return True
    return False



def fn_1(x):
    return sum([in_1(*y) for y in pre(x)])


def in_2(a, b, c, d):
    if c <= a <= d:
        return True
    if c <= b <= d:
        return True
    if a <= c <= b:
        return True
    if a <= d <= b:
        return True
    return False

def fn_2(x):
    return sum([in_2(*y) for y in pre(x)])
    
            
    
    
    
print(fn_1(x))
print(fn_2(x))