from utils import read_input, read_test
from dataclasses import dataclass
from typing import Optional
import numpy as np

x = read_input(8)
x_ = read_test(8)

@dataclass
class Tree:
    above: Optional[int]
    below: Optional[int]
    left: Optional[int]
    right: Optional[int]
        
def pre(x):
    out = []
    for r in x:
        out.append([int(y) for y in r])
    return np.array(out)
        

def fn_1(x):
    x = pre(x)
    n = 0
    for i in range(len(x)):
        for j in range(len(x[0])):
            val = x[i][j]
            if val > max(list(x[i][:j]) + [-1]):
                n+=1
                continue
            # right
            elif val > max(list(x[i][j+1:]) + [-1]):
                n+=1
                continue
            elif val > max(list(x[:,j][:i]) + [-1]):
                n+=1
                continue
            elif val > max(list(x[:,j][i+1:]) + [-1]):
                n+=1
                continue

    return n


print(fn_1(x))

def score(x, i, j):
    def fn_(trees, val):
        s = 0
        for t in trees:
            if t < val:
                s += 1
            else:
                s += 1
                break
        return s
    
    s = 1
    val = x[i][j]
 
    
    left = reversed(list(x[i][:j]))
    right = list(x[i][j+1:])
    up = reversed(list(x[:,j][:i]))
    down = list(x[:,j][i+1:])
    
    s *= fn_(left, val)    
    s *= fn_(right, val) 
    s *= fn_(up, val)
    s *= fn_(down, val)
    
    return s
    


def fn_2(x):
    x = pre(x)
    s = 0
    for i in range(len(x)):
        for j in range(len(x[0])):
            s_ = score(x, i, j)
            if s_ > s:
                s = s_
    return s

print(fn_2(x))