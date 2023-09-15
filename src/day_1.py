from dataclasses import dataclass
from collections import defaultdict
from typing import Any, Optional, Callable
import math
import copy
import ast
import functools
import numpy as np

from utils import read_input, read_test

x = read_input(1)

def fn_1(x):
    max_ = 0
    sum_ = 0
    for thing in x:
        if thing == '':
            if sum_ > max_:
                max_ = sum_
            sum_ = 0
        else:
            sum_ += int(thing)
    return max_

print(fn_1(x))

def fn_2(x):
    sums = []
    sum_ = 0
    for thing in x:
        if thing == '':
            sums.append(sum_)
            sum_ = 0
        else:
            sum_ += int(thing)
    return sum(sorted(sums)[-3:])

print(fn_2(x))
            
            
    

