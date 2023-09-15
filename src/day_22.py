from utils import read_input, read_test
import copy
import numpy as np
from dataclasses import dataclass

def read_input(day):
    with open(f'./aoc/input_{day}.txt', 'r') as f:
        x = [s[:-1] for s in f.readlines()]
    return x


def read_test(day):
    with open(f'./aoc/input_{day}_test.txt', 'r') as f:
        x = [s[:-1] for s in f.readlines()]
    return x

x = read_input(22)
x_ = read_test(22)

def pre(x):
    map_ = x[:-2]
    code = x[-1]
    
    
    ncols = max(len(thing) for thing in map_)
    arr = np.zeros((len(map_), ncols))
    for i, row in enumerate(map_):
        for j, elt in enumerate(row):
            if elt == '.':
                arr[i][j] = 1
            elif elt == '#':
                arr[i][j] = 2   
    
    turn_directions = {}
    for i, thing in enumerate(code):
        if thing in {'L', 'R'}:
            turn_directions[i] = thing
            
    return arr, code, turn_directions

def get_start(arr):
    return (0, min(i for i, x in enumerate(arr[0]) if x))

def rotate(curr, t):
    assert t in {'L', 'R'}
    if t == 'R':
        if curr == 'R':
            return 'D'
        elif curr == 'D':
            return 'L'
        elif curr == 'L':
            return 'U'
        else:
            return 'R'
    else:
        if curr == 'R':
            return 'U'
        elif curr == 'U':
            return 'L'
        elif curr == 'L':
            return 'D'
        else:
            return 'R'
        
def move_right(arr, rc, steps):
    # only handles move right
    r, c = rc
    start_idx = min(i for i, x in enumerate(arr[r]) if x)
    for _ in range(steps):
        next_ = (c+1)%len(arr[0])
        if not arr[r][next_]:
            if arr[r,start_idx] == 2:
                break
            else:
                c = start_idx
        elif arr[r,next_]==2:
            # stop
            break
        else:
            c=next_
    return r, c


def move_left(arr, rc, steps):
    r, c = rc
    last_idx = max(i for i, x in enumerate(arr[r]) if x)
    for _ in range(steps):
        next_ = c-1
        if not arr[r][next_]:
            if arr[r,last_idx] == 2:
                break
            else:
                c = last_idx
        elif arr[r,next_]==2:
            # stop
            break
        else:
            c=next_
    return r, c


def move_down(arr, rc, steps):
    r, c = rc
    start_idx = min(i for i, x in enumerate(arr[:,c]) if x)
    for _ in range(steps):
        next_ = (r+1)%len(arr)
        if not arr[next_][c]:
            if arr[start_idx,c] == 2:
                break
            else:
                r = start_idx
        elif arr[next_,c]==2:
            # stop
            break
        else:
            r = next_
    return r, c


def move_up(arr, rc, steps):
    r, c = rc
    last_idx = max(i for i, x in enumerate(arr[:,c]) if x)
    for _ in range(steps):
        next_ = (r-1)
        if not arr[next_][c]:
            if arr[last_idx,c] == 2:
                break
            else:
                r = last_idx
        elif arr[next_,c]==2:
            # stop
            break
        else:
            r = next_
    return r, c


move_handler = {
    'L': move_left,
    'R': move_right,
    'U': move_up,
    'D': move_down,
}
        

def fn_1(x):
    arr, code, turns = pre(x)
    
    t_ = -1
    c = 'R'
    rc = get_start(arr)
    for t in turns:
        steps = int(code[t_+1:t])
        rc = move_handler[c](arr, rc, steps)
        c = rotate(c, turns[t])
        t_ = t
    if t_ < len(code) - 1:
        steps = int(code[t_+1:])
        rc = move_handler[c](arr, rc, steps)
    
    if c == 'R':
        c_ = 0
    elif c == 'D':
        c_ = 1
    elif c == 'L':
        c_ = 2
    else:
        c_ = 3
    return (1000*(rc[0]+1))+(4*(rc[1]+1))+c_
    
print(fn_1(x))

class Arr:
    def __init__(self, arr):
        self.arr = copy.deepcopy(arr)
        
    def __repr__(self):
        out = ''
        for row in self.arr:
            rowstr = ''
            for elt in row:
                if elt == 0:
                    rowstr+=' '
                elif elt == 1:
                    rowstr+='.'
                elif elt == 2:
                    rowstr+='#'
                else:
                    rowstr+='@'
            rowstr += '\n'
            out += rowstr
        return out
                    
    def put(self, rc, face):
        r, c = remap(rc, face)
        self.arr[r, c] = 3

def pre(x):
    map_ = x[:-2]
    code = x[-1]
    
    
    ncols = max(len(thing) for thing in map_)
    arr = np.zeros((len(map_), ncols))
    for i, row in enumerate(map_):
        for j, elt in enumerate(row):
            if elt == '.':
                arr[i][j] = 1
            elif elt == '#':
                arr[i][j] = 2  
    
    yu = arr[:50,50:100]
    xr = arr[:50,100:]
    zd = arr[50:100,50:100]
    yd = arr[100:150,50:100]
    xl = arr[100:150,:50]
    zu = arr[150:,:50]
    
    @dataclass
    class _C:
        R: int
        L: int
        U: int
        D: int

    faces = {
        'yu': yu,
        'yd': yd,
        'xl': xl,
        'xr': xr,
        'zu': zu,
        'zd': zd,
    }
    
    graph = {
        'yu': _C(('xr', 'lrn'), ('xl', 'lrnf'), ('zu', 'lra'), ('zd', 'udn')),
        'yd': _C(('xr', 'rlnf'), ('xl', 'rln'), ('zd', 'dun'), ('zu', 'rla')),
        'xl': _C(('yd', 'lrn'), ('yu', 'lrnf'), ('zd', 'lra'), ('zu', 'udn')),
        'xr': _C(('yd', 'rlnf'), ('yu', 'rln'), ('zu', 'dun'), ('zd', 'rla')),
        'zu': _C(('yd', 'dua'), ('yu', 'uda'), ('xl', 'dun'), ('xr', 'udn')),
        'zd': _C(('xr', 'dua'), ('xl', 'uda'), ('yu', 'dun'), ('yd', 'udn')),
    }
    graph = Graph(graph)

    turn_directions = {}
    for i, thing in enumerate(code):
        if thing in {'L', 'R'}:
            turn_directions[i] = thing
            
    return faces, graph, code, turn_directions, Arr(arr)


@dataclass
class Graph:
    graph: dict
        
    d2i = {
        'R': (0,1),
        'L': (0,-1),
        'U': (-1,0),
        'D': (1,0),    
    }
    
    def jump(self, face, r, c, direction):
        face_, stuff = getattr(self.graph[face], direction)
        direction_ = stuff[1].upper()
        entry_side = stuff[0]
        transpose = stuff[2] == 'a'
        flipped = len(stuff) == 4
        if entry_side == 'r':
            c_ = 49
            thing = r if not transpose else c
            r_ = thing if not flipped else (49-thing)
        elif entry_side == 'l':
            c_ = 0
            thing = r if not transpose else c
            r_ = thing if not flipped else (49-thing)
        elif entry_side == 'u':
            r_ = 0
            thing = c if not transpose else r
            c_ = thing if not flipped else (49-thing)
        else:
            assert entry_side == 'd'
            r_ = 49
            thing = c if not transpose else r
            c_ = thing if not flipped else (49-thing)
        return face_, r_, c_, direction_
    
    def update(self, face, r, c, direction):
        r_, c_ = r+self.d2i[direction][0], c+self.d2i[direction][1]
        if r_ < 0 or c_ < 0 or r_ >= 50 or c_ >= 50:
            face_, r_, c_, direction = self.jump(face, r, c, direction)
            return face_, r_, c_, direction
        else:
            return face, r_, c_, direction


def move(face, rc, direction, faces, graph, steps, arr):
    r, c = rc
    arr.put((r, c), face)
    #import pdb; pdb.set_trace()
    for _ in range(steps):
        face_, r_, c_, direction_ = graph.update(face, r, c, direction)
        if faces[face_][r_, c_] == 2:
            break
        else:
            face, r, c, direction = face_, r_, c_, direction_
            arr.put((r, c), face)
    return face, (r,c), direction


def remap(rc, face):
    r, c = rc
    if face == 'yu':
        return r, c+50
    elif face == 'xr':
        return r, c+100
    elif face == 'zd':
        return r+50, c+50
    elif face == 'xl':
        return r+100, c
    elif face == 'yd':
        return r+100, c+50
    elif face == 'zu':
        return r+150, c
        

    
def fn_2(x):
    faces, graph, code, turns, arr = pre(x)
    
    t_ = -1
    direction = 'R'
    rc = (0, 0)
    face = 'yu'
    for t in turns:
        steps = int(code[t_+1:t])
        face, rc, direction = move(face, rc, direction, faces, graph, steps, arr)
        direction = rotate(direction, turns[t])
        t_ = t
    if t_ < len(code) - 1:
        steps = int(code[t_+1:])
        face, rc, direction = move(face, rc, direction, faces, graph, steps, arr)
    
    rc = remap(rc, face)
    if direction == 'R':
        c_ = 0
    elif direction == 'D':
        c_ = 1
    elif direction == 'L':
        c_ = 2
    else:
        c_ = 3
    return (1000*(rc[0]+1))+(4*(rc[1]+1))+c_

print(fn_2(x))