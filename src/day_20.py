from utils import read_input, read_test
from dataclasses import dataclass
from typing import Any

x = read_input(20)
x_ = read_test(20)

def pre(x):
    nodes = {}
    for i, elt in enumerate(x):
        nodes[i] = Node(i, int(elt), None, None)
        
    for k, v in nodes.items():
        prev = (k-1)%len(x)
        child = (k+1)%len(x)
        v.parent = nodes[prev]
        v.child = nodes[child]
        
    nodes[0].start=True
    nodes[i].end=True
    return nodes
        

@dataclass
class Node:
    original_idx: int
    val: int
    parent: Any
    child: Any
    start: bool = False
    end: bool = False
        
    def __repr__(self):
        return f'original index: {self.original_idx}, value: {self.val}, parent: {self.parent.original_idx}, child: {self.child.original_idx}. start: {self.start}, end: {self.end}'
        

def move_right(node, n):
    n = abs(n)
    for _ in range(n):
        # we are b
        # a<--->b<-->c<--->d<----
        # to
        # a<--->c<-->b<--->d<---
        a = node.parent
        b = node
        c = node.child
        d = node.child.child
        
        a.child = c
        c.parent = a
        c.child = b
        b.parent = c
        b.child = d
        d.parent = b
        
        if c.end:
            assert d.start
            d.start = False
            b.start = True    
        elif b.start:
            assert a.end
            b.start = False
            c.start = True  
        elif b.end:
            assert c.start
            b.end = False
            a.end = True
            


def move_left(node, n):
    n = abs(n)
    
    for _ in range(n):
        # we are c
        # a<--->b<-->c<--->d<----
        # to
        # a<--->c<-->b<--->d<---
        
        c = node
        d = node.child
        b = node.parent
        a = b.parent
        
        a.child=c
        c.parent=a
        c.child=b
        b.parent=c
        b.child=d
        d.parent=b
    
        
        if b.start:
            assert a.end
            a.end = False
            c.end=True      
        elif c.end:
            assert d.start
            c.end = False
            b.end=True
        elif c.start:
            assert b.end
            c.start=False
            d.start=True
            
        
            
            
            
            
def order(nodes):
    out = []
    for n in nodes.values():
        if n.start:
            curr = n
            while not curr.end:
                out.append(str(curr.val) + f'{"" if not curr.start else " (start)"}')
                curr = curr.child
            out.append(str(curr.val) + f'{"" if not curr.end else " (end)"}')
    return out


def order_(nodes):
    out = []
    for n in nodes.values():
        if n.start:
            curr = n
            while not curr.end:
                out.append(curr.val)
                curr = curr.child
            out.append(curr.val)
    return out


def get(arr, idx):
    for i, elt in enumerate(arr):
        if elt == 0:
            break
    next_ = (i + idx)%len(arr)
    return arr[next_]

            
        

def fn_1(x):
    nodes = pre(x)
    
    for node in nodes.values():
        if node.val > 0:
            move_right(node, node.val)
        elif node.val < 0:
            move_left(node, node.val)
        else:
            pass
        
    thing = order_(nodes)
    
    return get(thing, 1000) + get(thing, 2000) + get(thing, 3000)


print(fn_1(x))


def pre_2(x):
    code = 811589153
    nodes = {}
    for i, elt in enumerate(x):
        nodes[i] = Node(i, int(elt)*code, None, None)
        
    for k, v in nodes.items():
        prev = (k-1)%len(x)
        child = (k+1)%len(x)
        v.parent = nodes[prev]
        v.child = nodes[child]
        
    nodes[0].start=True
    nodes[i].end=True
    return nodes


def fn_2(x):
    nodes = pre_2(x)
    
    for i in range(10):
        for node in nodes.values():
            actual = abs(node.val)%(len(nodes)-1)
            if node.val > 0:
                move_right(node, actual)
            elif node.val < 0:
                move_left(node, actual)
            else:
                pass   
    thing = order_(nodes)
    
    return get(thing, 1000) + get(thing, 2000) + get(thing, 3000)


print(fn_2(x))