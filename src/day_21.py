from utils import read_input, read_test
from typing import Any
from dataclasses import dataclass

x = read_input(21)


@dataclass
class Monkey:
    name: str
    val: Any
    first: Any
    op: Any
    second: Any
        

def pre(x):
    monkeys = {}
    for m in x:
        m = m.split(' ')
        assert len(m) <= 4
        name = m[0][:-1]
        if len(m) == 2:
            monkeys[name] = Monkey(name, int(m[1]), None, None, None)
        else:
            monkeys[name] = Monkey(name, None, m[1], m[2], m[3])
    return monkeys


def calculate(monkeys, mname):
    m = monkeys[mname]
    if m.val:
        return m.val
    else:
        op = m.op
        left = m.first
        right = m.second
        if op == '+':
            return calculate(monkeys, left) + calculate(monkeys, right)
        elif op == '-':
            return calculate(monkeys, left) - calculate(monkeys, right)
        elif op == '*':
            return calculate(monkeys, left) * calculate(monkeys, right)
        elif op == '/':
            return calculate(monkeys, left) / calculate(monkeys, right)
        elif op == '=':
            left = (calculate(monkeys, left))
            right = (calculate(monkeys, right))
            return int(left == right), left, right
 

def fn_1(x):
    monkeys = pre(x)
    return int(calculate(monkeys, 'root'))


print(fn_1(x))


def fn_2(x):
    monkeys = pre(x)
    monkeys['root'].op = '='
    equal, _, _ = calculate(monkeys, 'root')
    lower = 420
    upper_bound_found = False
    upper = 420
    guess = lower
    i = 0
    while not equal and i < 300:
        if not upper_bound_found:
            upper = upper*2
            guess = upper
            monkeys['humn'].val = guess
            equal, left, right = calculate(monkeys, 'root')
            if left < right:
                upper_bound_found=True
        else:
            guess = int(upper + lower)/2
            monkeys['humn'].val = guess
            equal, left, right = calculate(monkeys, 'root')
            if left > right:
                lower = guess
            if left < right:
                upper = guess
        i+=1
            
    return int(guess)
                  
    
print(fn_2(x))
       