from utils import read_input, read_test


x = read_input(3)

def priority(x):
    if x.isupper():
        x = x.lower()
        return (ord(x) - ord('a') + 1) + 26
    else:
        return (ord(x) - ord('a') + 1)



def fn_1(x):
    s = 0
    for r in x:
        middle = int(len(r)/2)
        common = set(r[0:middle]).intersection(set(r[middle:]))
        assert len(common) == 1
        s += priority(common.pop())
    return s

print(fn_1(x))

def fn_2(x):
    i = 0
    s = 0
    while i < len(x):
        e0, e1, e2 = x[i:i+3]
        common = set(e0).intersection(set(e1)).intersection(set(e2))
        assert len(common) == 1
        s += priority(common.pop())
        i += 3
    return s

print(fn_2(x))