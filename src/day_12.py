from utils import read_input, read_test
import copy

x = read_input(12)
x_ = read_test(12)

def pre(x):
    out = []
    for row in x:
        out.append(list(row))
    return out

def find(start, grid):
    t = copy.deepcopy(grid)
    H = len(grid) - 1
    W = len(grid[0]) - 1
    nodes = [(*start, 0)]
    while nodes:
        i, j, d = nodes.pop(0)
        val = grid[i][j]
        if val == 'E':
            return d
        elif isinstance(val, str): # means did not get explored in the meantime
            above = (i-1, j)
            below = (i+1, j)
            left = (i, j-1)
            right = (i, j+1)
            
            potential_neighbors = [above, below, left, right]
            for r, c in potential_neighbors:
                if r <= H and c <= W and r >= 0 and c >= 0:
                    if isinstance(grid[r][c], str) and ord(grid[r][c]) <= ord(val)+1:  # means unexplored
                        if grid[r][c] == 'E':
                            if val in ('y', 'z'):
                                nodes.append((r, c, d+1)) 
                        else:
                            nodes.append((r, c, d+1))             
    
            grid[i][j] = (grid[i][j], d) # mark node as visited

        

def fn_1(x):
    x = pre(x)
    for i in range(len(x)):
        break_ = False
        for j in range(len(x[0])):
            if x[i][j] == 'S':
                break_ = True
                break
        if break_:
            break
    
    nodes = []
    x[i][j] = 'a'
    return find((i, j), x)

print(fn_1(x))


def fn_2(x):
    x = pre(x)
    starting_points = []
    for i in range(len(x)):
        for j in range(len(x[0])):
            if x[i][j] in ('S', 'a'):
                starting_points.append((i, j))
    
    o = 1000000000000000
    for sp in starting_points:
        x_ = copy.deepcopy(x)
        out = find(sp, x_)
        if out and out < o:
            o = out
    return o

print(fn_2(x))