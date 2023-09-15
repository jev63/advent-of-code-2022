from utils import read_input, read_test

x = read_input(25)
x_ = read_test(25)


def s2n(x):
    out = 0
    for i, digit in enumerate(reversed(x)):
        if digit in {'2', '1', '0'}:
            digit = int(digit)
        elif digit == '-':
            digit = -1
        else:
            assert digit == '='
            digit = -2
        s = (5**i)*digit
        out+=s
    return out
    

def _fn(x):
    if x == 0:
        return (0,0,0)

    x = int(x)
    e = -1
    smaller=True
    while smaller:
        block = 5**(e+1)
        if block <= x:
            e+=1
        else:
            smaller=False
    c = 0
    smaller=True
    while smaller:
        block = (c+1)*(5**e)
        if block <= x:
            c+=1
        else:
            smaller=False

    assert c < 5
    if c == 3:
        r = -2
        c = 1
        e +=1
    elif c == 4:
        r = -1
        c = 1
        e+=1
    else:
        r = 0
    return e, c, r


def post(x):
    good = {-2,-1,0,1,2}
    bad = any(t not in good for t in x)
    while bad:
        if x[0] == 3:
            x[0] = -2
            x.insert(0,1)
        elif x[0] == 4:
            x[0] = -1
            x.insert(0,1)

        bad = False
        for i, entry in enumerate(x):
            if entry == 3:
                x[i] = -2
                x[i-1]+=1
                bad = True
                break
            elif entry == 4:
                x[i] = -1
                x[i-1]+=1
                bad = True
                break

    return x

    
def n2s(x):
    things = []
    e, c, r = _fn(x)
    things.append((e, c, r))
    resid = abs(x - ((c*(5**e))+int(r*(5**(e-1)))))
    while resid > 0:
        e, c, r = _fn(resid)
        things.append((e, c, r))
        resid = abs(resid - ((c*(5**e))+int(r*(5**(e-1)))))
        
    max_e = max(e for e, _, _ in things)
    out = [0]*(max_e+1)
    for e, c, r in things:
        out[e] += c
        out[e-1] += r
        
    out = list(reversed(out))
        
    out = post(out)
    
    return ''.join([str(x) if x >= 0 else '-' if x == -1 else '=' for x in out])

    
def fn(x):
    sums = []
    for s in x:
        n = s2n(s)
        sums.append(n)
    return n2s(sum(sums))

print(fn(x))