from utils import read_input, read_test
from dataclasses import dataclass

x = read_input(18)
x_ = read_test(18)

def pre(x):
    return set(x)

def fn_1(x):
    out = 0
    x_ = pre(x)
    for cube in x:
        x, y, z = [int(x) for x in cube.split(',')]
        adjacent = [
            f'{x-1},{y},{z}',
            f'{x+1},{y},{z}',
            f'{x},{y-1},{z}',
            f'{x},{y+1},{z}',
            f'{x},{y},{z-1}',
            f'{x},{y},{z+1}',
        ]
        for a in adjacent:
            if a not in x_:
                out+=1
    return out

print(fn_1(x))


def pre_2(x):
    return set(tuple(int(coord) for coord in point.split(',')) for point in x) 


@dataclass
class Filler:
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int
    drops: set
        
    def in_(self, pt):
        x, y, z = pt
        if x >=(self.xmin-1) and x <= (self.xmax+1):
            if y >=(self.ymin-1) and y <= (self.ymax+1):
                if z >=(self.zmin-1) and z <= (self.zmax+1):
                    return True
        return False
            
    
    def fill(self, contour, pt):
        to_process = []
        to_process.append(pt)
        while to_process:
            pt = to_process.pop()
            contour.add(pt)
            x, y, z = pt
            neighbors = [
                (x-1, y, z),
                (x+1, y, z),
                (x, y-1, z),
                (x, y+1, z),
                (x, y, z-1),
                (x, y, z+1),
            ]

            neighbors = [n for n in neighbors if self.in_(n) and (n not in self.drops) and (n not in contour)]
            to_process.extend(neighbors)


def fn_2(x):
    drops = pre_2(x)   
    xmin, xmax = min(x for x, _, _ in drops),  max(x for x, _, _ in drops)
    ymin, ymax = min(y for _, y, _ in drops),  max(y for _, y, _ in drops)
    zmin, zmax = min(z for _, _, z in drops),  max(z for _, _, z in drops)
    

    f = Filler(xmin, xmax, ymin, ymax, zmin, zmax, drops)
    contour = set()
    f.fill(contour, (1,1,1))
    
    out = 0
    for x, y, z in drops:
        adjacent = [
            (x-1, y, z),
            (x+1, y, z),
            (x, y-1, z),
            (x, y+1, z),
            (x, y, z-1),
            (x, y, z+1),
        ]
        for a in adjacent:
            if a in contour:
                out+=1

    return out
        
print(fn_2(x))