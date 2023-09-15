from utils import read_input, read_test
from dataclasses import dataclass
import numpy as np

x = read_input(10)
x_ = read_test(10)


@dataclass
class State:
    val: int
    op: str
    cycle: int
    state: str='finished'

def update_noop(s):
    s.state='started'
    s.op='noop'
    s.cycle += 1
    if s.cycle == 20 or ((s.cycle - 20) % 40 == 0):
        out = s.val * s.cycle
    else:
        out = 0
    s.state='finished'
    return out
    
def update_add_1st_cycle(s):
    s.state='started'
    s.op='addx'
    s.cycle+=1
    if s.cycle == 20 or ((s.cycle - 20) % 40 == 0):
        out = s.val * s.cycle
    else:
        out=0
    s.state='finished'
    return out
    
def update_add_2nd_cycle(s, a):
    s.state='started'
    s.op='addx'
    s.cycle+=1
    if s.cycle == 20 or ((s.cycle - 20) % 40 == 0):
        out = s.val * s.cycle
    else:
        out=0
    s.state='finished'
    s.val += a
    return out

def fn_1(x):
    s = State(val=1, op=None, cycle=0)
    out = 0
    for i, op in enumerate(x, 1):
        if op.startswith('noop'):
            y = update_noop(s)
            out+=y
        else:
            a = int(op.split(' ')[-1])
            y = update_add_1st_cycle(s)
            out+=y
            y = update_add_2nd_cycle(s, a)
            out+=y
    return out
                
print(fn_1(x))



def update_noop_2(s):
    s.state='started'
    s.op='noop'
    s.cycle += 1
    out = (s.cycle % 40) in (s.val, s.val+1, s.val-1)
    s.state='finished'
    return out
    
def update_add_1st_cycle_2(s):
    s.state='started'
    s.op='addx'
    s.cycle+=1
    out = (s.cycle % 40) in (s.val, s.val+1, s.val-1)
    s.state='finished'
    return out
    
def update_add_2nd_cycle_2(s, a):
    s.state='started'
    s.op='addx'
    s.cycle+=1
    s.state='finished'
    s.val += a
    out = (s.cycle % 40) in (s.val, s.val+1, s.val-1)
    return out


def fn_2(x):
    s = State(val=1, op=None, cycle=0)
    out = [0]*(40*6)
    for i, op in enumerate(x, 1):
        if op.startswith('noop'):
            y = update_noop_2(s)
            if y:
                out[s.cycle-1] = 1            
        else:
            a = int(op.split(' ')[-1])
            y = update_add_1st_cycle_2(s)
            if y:
                out[s.cycle-1] = 1
            y = update_add_2nd_cycle_2(s, a)
            if y:
                out[s.cycle-1] = 1
    g = np.array(out).reshape(6, 40)
    for line in g:
        print(''.join(['.'if x == 0 else '#' for x in line]))


fn_2(x)
           