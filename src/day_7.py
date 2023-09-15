from utils import read_input, read_test
from dataclasses import dataclass
from typing import Any

x = read_input(7)
x_ = read_test(7)

@dataclass
class Dir:
    name: str
    subdirs: list
    files: list
    parent: Any
    size: int = 0
        
def pre(x):
    root = Dir('/', [], [], None)
    cwd = root
    for cmd in x:
        if cmd == '$ ls':
            continue
        elif cmd == '$ cd ..':
            cwd = cwd.parent
            continue
        elif cmd == '$ cd /':
            cwd = root
            continue
        elif 'cd ' in cmd:
            nwd = cmd.split(' ')[-1]
            for subdir in cwd.subdirs:
                if subdir.name == nwd:
                    cwd = subdir
                    break
            continue
        elif 'dir ' in cmd:
            cwd.subdirs.append(Dir(cmd.split(' ')[-1], [], [], cwd))
            continue
        else:
            size, name = cmd.split(' ')
            cwd.files.append(int(size))
    return root


def size(x):
    if x.subdirs == []:
        x.size = sum(x.files)
    else:
        [size(y) for y in x.subdirs]
        x.size = sum(y.size for y in x.subdirs) + sum(x.files)
        
        
def ls(x, sizes):
    sizes.append(x.size)
    for subdir in x.subdirs:
        ls(subdir, sizes)
        

def fn_1(x):
    x = pre(x[1:])
    size(x)
    sizes = []
    ls(x, sizes)
    return sum([y for y in sizes if y <=100000])


print(fn_1(x))


def fn_2(x):
    x = pre(x[1:])
    size(x)
    sizes = []
    ls(x, sizes)
    
    total = 70000000
    needed = 30000000
    root_size = x.size
    
    avail = total - root_size
    need_to_delete = needed - avail
    
    return sorted([y for y in sizes if y >= need_to_delete])[0]


print(fn_2(x))
    