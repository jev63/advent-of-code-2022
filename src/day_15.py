from utils import read_input, read_test
from tqdm import tqdm


x = read_input(15)
x_ = read_test(15)


def pre(x):
    out = []
    for row in x:
        row = row.split(' ')
        x1, y1 = row[2], row[3]
        x2, y2 = row[8], row[9]
        x1 = int(''.join(x1.split('=')[1][:-1]))
        y1 = int(''.join(y1.split('=')[1][:-1]))
        x2 = int(''.join(x2.split('=')[1][:-1]))
        y2 = int(''.join(y2.split('=')[1]))

        out.append([(x1, y1), (x2, y2)])
        
    return out


def dist(p1, p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])


def post(intervals):
    intervals = sorted(intervals)
    merged = [intervals[0]]
    for i in range(1, len(intervals)):
        s1, e1 = merged[-1]
        s2, e2 = intervals[i]
        if s2 <= e1+1:
            merged[-1] = (s1, max(e2, e1))
        else:
            merged.append((s2, e2))

    return merged


def sum_up(intervals):
    out = 0
    for s, e in intervals:
        out += e-(s-1)
    return out
        

    
def beaconless(y, bs):
    intervals = []
    for [(x1, y1), (x2, y2)] in bs:
        d = dist((x1, y1), (x2, y2))
        p = dist((x1, y1), (x1, y))
        if p > d:
            continue
        else:
            r = d - p
            intervals.append((x1-(r), x1+(r)))
            
    return post(intervals)
      
        
def fn_1(x):
    x = pre(x)
    return sum_up(beaconless(10, x)) - len(set(b[1] for _, b in x if b[1] == 10))
    
    
print(fn_1(x_))


def fn_2(x):
    x = pre(x)
    for i in tqdm(range(4000001)):
        intervals = beaconless(i, x)
        if len(intervals) > 1:
            return ((intervals[0][-1]+1)*4000000) + i

        
        
print(fn_2(x))
