from utils import read_input, read_test
from dataclasses import dataclass
from typing import Callable, Any
import math

x = read_input(11)
x_ = read_test(11)

@dataclass
class Monkey:
    name: str
    items: list
    operation: Callable
    test: Callable
    passing: Any
    failing: Any
    n_inspections: int = 0
        
    def reduce(x):
        return math.floor(x / 3)
        
    def __post_init__(self):
        self.n_items = len(self.items)
        
    def __repr__(self):
        return str([self.name, self.items, self.passing.name, self.failing.name,  self.n_inspections])
    
        
        
    @staticmethod
    def operation_creator(multiply, val):
        if multiply:
            if val == 'old':
                return lambda x: x**2
            else:
                return lambda x: x * int(val)
        else:
            if val == 'old':
                return lambda x: x + x
            else:
                return lambda x: x + int(val)
        
    @classmethod
    def from_input(cls, m):
        name = m[0][-2]
        items = [int(item) for item in m[1].split(':')[-1].strip().split(', ')]
        operation = cls.operation_creator(m[2].split(' ')[-2] == '*', m[2].split(' ')[-1])
        test = lambda x: x % int(m[3].split(' ')[-1]) == 0
        passing = m[4][-1]
        failing = m[5][-1]
        return cls(name, items, operation, test, passing, failing)

    
    def turn(self):
        for _ in range(len(self.items)):
            self.n_inspections += 1
            item = self.items.pop(0)
            item_ = self.operation(item)
            item__ = Monkey.reduce(item_)
            if self.test(item__):
                self.passing.items.append(item__)
            else:
                self.failing.items.append(item__)
                
    def turn_2(self):
        for _ in range(len(self.items)):
            self.n_inspections += 1
            item = self.items.pop(0)
            item_ = self.operation(item)
            item__ = item_ % 9699690
            if self.test(item__):
                self.passing.items.append(item__)
            else:
                self.failing.items.append(item__)
                
def pre(x):
    monkeys = [x[0:6], x[7:13], x[14:20], x[21:27], x[28:34], x[35:41], x[42:48], x[49:55]]
    m0, m1, m2, m3, m4, m5, m6, m7 = monkeys
    out = {}
    for m in monkeys:
        m_ = Monkey.from_input(m)
        out[m_.name] = m_
    
    out_ = []
    for m in out.values():
        m.passing = out[m.passing]
        m.failing = out[m.failing]
        out_.append(m)
    return out_


def fn_1(x):
    monkeys = pre(x)

    
    for i in range(20):
        for m in monkeys:
            m.turn()
            
    a, b = sorted(m.n_inspections for m in monkeys)[-2:]
    return a*b


print(fn_1(x))



def fn_2(x):
    monkeys = pre(x)

    
    for i in range(10000):
        for m in monkeys:
            m.turn_2()
            
    a, b = sorted(m.n_inspections for m in monkeys)[-2:]
    return a*b


print(fn_2(x))
    