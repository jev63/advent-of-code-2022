from utils import read_input, read_test
from collections import defaultdict

x = read_input(23)
x_ = read_test(23)


def pre(x):
    elves = set()
    for r in range(len(x)):
        for c in range(len(x[0])):
            if x[r][c] == '#':
                elves.add((r,c))
    return elves

N = lambda r,c: ([(r-1, c-1), (r-1, c), (r-1, c+1)], (r-1,c))
S = lambda r,c: ([(r+1, c-1), (r+1, c), (r+1, c+1)], (r+1,c))
W = lambda r,c: ([(r-1, c-1), (r, c-1), (r+1, c-1)], (r, c-1))
E = lambda r,c: ([(r-1, c+1), (r, c+1), (r+1, c+1)], (r, c+1))

ORDER = [N,S,W,E]


def propose_move(elf, i, elves):
    r, c = elf
    options = [(r-1,c-1),(r-1,c),(r-1,c+1),(r,c-1),(r,c+1),(r+1,c-1),(r+1,c),(r+1,c+1)]
    must_move = any(o in elves for o in options)

    if must_move:
        for j in range(4):
            rule = (i+j)%len(ORDER)
            options, outcome = ORDER[rule](r,c)
            doable = not any(o in elves for o in options)
            if doable:
                return outcome
    

def fn_1(x):
    elves = pre(x)
    
    for i in range(10):
        d = defaultdict(list)
        for elf in elves:
            move = propose_move(elf, i, elves)
            # move can be none if elf is good where he is
            # or if he cant move anywhere
            if move:
                d[str(move)].append(elf)
        for m, e in d.items():
            m = tuple(int(thing) for thing in m[1:-1].split(', '))
            if len(e) == 1:
                elves -= set(e)
                elves.add(m)
    
    xmin = min(e[0] for e in elves)
    xmax = max(e[0] for e in elves)
    ymin = min(e[1] for e in elves)
    ymax = max(e[1] for e in elves)
    
    xdist = xmax - (xmin-1)
    ydist = ymax - (ymin-1)
    
    return xdist*ydist-len(elves)
                

print(fn_1(x))


def fn_2(x):
    elves = pre(x)
    
    needed = True
    iters = 0
    
    while needed:
        d = defaultdict(list)
        for elf in elves:
            move = propose_move(elf, iters, elves)
            # move can be none if elf is good where he is
            # or if he cant move anywhere
            if move:
                d[str(move)].append(elf)
        for m, e in d.items():
            m = tuple(int(thing) for thing in m[1:-1].split(', '))
            if len(e) == 1:
                elves -= set(e)
                elves.add(m)
        iters+=1
        needed = len(d) > 0
    
    return iters

print(fn_2(x))