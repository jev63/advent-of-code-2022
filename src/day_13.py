from utils import read_input, read_test
import ast
import copy
import functools

x = read_input(13)
x_ = read_test(13)


def pre_1(x):
    out = []
    for i in range(0,len(x),3):
        left = ast.literal_eval(x[i])
        right = ast.literal_eval(x[i+1])
        out.append((left, right))
    return out


def compare(a, b):
    if a == [] and b == []:  # ee
        return 'keep going'
    elif a == [] and b != []:  # e ne, e i
        return True
    elif a != [] and b == []:  # ne e, i e
        return False
    elif isinstance(a, int) and isinstance(b, int):  # ii
        if a < b:
            return True
        elif a == b:
            return 'keep going'
        else:
            return False
    elif isinstance(a, int) and isinstance(b, list): # i e (but already handled), i ne
        a_1 = [a]
        return compare(a_1, b)
    elif isinstance(a, list) and isinstance(b, int):  # ne i, e i (but already handled)
        b_1 = [b]
        return compare(a, b_1)
    else: # ne ne
        assert isinstance(a, list) and isinstance(b, list)
        a_0 = a.pop(0)
        b_0 = b.pop(0)
        c_0 = compare(a_0, b_0)
        if c_0 == 'keep going':
            return compare(a, b)
        else:
            if b:
                return c_0
            else:
                return c_0
    

def fn_1(x):
    out = []
    x = pre_1(x)
    for i, (a, b) in enumerate(x):
        if True:
            if compare(a, b):
                out.append(i+1)
        
    return sum(out)

print(fn_1(x))


def pre_2(x):
    out = []
    for i in range(0,len(x),3):
        left = ast.literal_eval(x[i])
        right = ast.literal_eval(x[i+1])
        out.append(left)
        out.append(right)
    out.append([[2]])
    out.append([[6]])
    return out

def compare_2(a, b):
    a_ = copy.deepcopy(a)
    b_ = copy.deepcopy(b)
    
    if compare(a_, b_):
        return -1
    else:
        return 1


def fn_2(x):
    x = sorted(pre_2(x), key=functools.cmp_to_key(lambda a, b: compare_2(a, b)))
    lower = -1
    upper = -2
    for i, y in enumerate(x):
        if y == [[2]]:
            lower = i+1
        elif y == [[6]]:
            upper = i+1
    return lower * upper
            
        
        
print(fn_2(x))