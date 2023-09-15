from utils import read_input, read_test

x = read_input(24)
x_ = read_test(24)

def pre(x):
    out = []
    for row in x:
        out.append(list(row))
    return out


def empty(x):
    out = []
    for row in x:
        out.append([thing if thing=='#' else '' for thing in row])
    return out


def get_new_coords(blizzard, r, c, nrows, ncols):
    if blizzard == '>':
        if c+1 == ncols-1:
            return (r,1)
        else:
            return (r,c+1)
    elif blizzard == '<':
        if c-1 == 0:
            return (r,ncols-2)
        else:
            return (r,c-1)
    elif blizzard == '^':
        if r-1 == 0:
            return (nrows-2, c)
        else:
            return (r-1,c)
    else:
        assert blizzard == 'v'
        if r+1 == nrows-1:
            return (1, c)
        else:
            return (r+1,c)
    

def step(x):
    nrows, ncols = len(x), len(x[0])
    new = empty(x)
    for r in range(1, nrows-1):
        for c in range(1, ncols-1):
            entry = x[r][c]
            if entry not in {'.', ''}:
                for blizzard in entry:
                    r_, c_ = get_new_coords(blizzard, r, c, nrows, ncols)
                    new[r_][c_] += blizzard
    return new

    
def get_options(next_field, curr_loc):
    nrows, ncols = len(next_field), len(next_field[0])
    r, c = curr_loc
    if (r, c) == (nrows-1, ncols-2):
        options = [(r,c),(r-1,c)]
    else:
        options = [(r-1,c),(r,c-1),(r,c+1),(r+1,c), (r,c)]
    return [(r_, c_) for (r_, c_) in options if next_field[r_][c_] in {'', '.'}] # and (r_,c_) != (0,1))]
    
    
def maze(field, loc, nsteps):
    nrows, ncols = len(field), len(field[0])
    next_field = step(field)
    my_options = get_options(next_field, loc)
    states = [[o, nsteps+1] for o in my_options]
    states_set = set(str(s) for s in states)
    maps = {}
    maps[0] = field
    maps[1] = next_field
    
    while states:
        thing = states.pop(0)
        states_set.remove(str(thing))
        loc, nsteps = thing
        field = maps[nsteps]
        if loc == (nrows-1, ncols-2):
            return nsteps
        else:
            if nsteps+1 not in maps:
                maps[nsteps+1] = step(field)
            my_options = get_options(maps[nsteps+1], loc)
            for o in my_options:
                literal = [o, nsteps+1]
                string = str(literal)
                if string not in states_set:
                    states.append(literal)
                    states_set.add(string)

    
def fn_1(x):
    x = pre(x)
    start = (0,1)
    return maze(x, start, 0)
    
print(fn_1(x))
    
def maze2(field, loc, nsteps):
    nrows, ncols = len(field), len(field[0])
    next_field = step(field)
    my_options = get_options(next_field, loc)
    states = [[o, nsteps+1] for o in my_options]
    states_set = set(str(s) for s in states)
    maps = {}
    maps[0] = field
    maps[1] = next_field
    
    stage = 1
    
    while states:
        thing = states.pop(0)
        states_set.remove(str(thing))
        loc, nsteps = thing
        field = maps[nsteps]
        if loc == (nrows-1, ncols-2) and stage==1:
            stage=2
            states_set=set()
            states=[]
        elif loc == (0,1) and stage==2:
            states_set=set()
            states=[]
            stage=3
        elif loc == (nrows-1, ncols-2) and stage==3:
            return nsteps 
        
        if nsteps+1 not in maps:
            maps[nsteps+1] = step(field)
        my_options = get_options(maps[nsteps+1], loc)
        for o in my_options:
            literal = [o, nsteps+1]
            string = str(literal)
            if string not in states_set:
                states.append(literal)
                states_set.add(string)


def fn_2(x):
    x = pre(x)
    start = (0,1)
    return maze2(x, start, 0)

print(fn_2(x))