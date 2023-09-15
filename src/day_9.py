from utils import read_input, read_test

x = read_input(9)
x_ = read_test(9)

def update_head(curr, d):
    old = [curr[0], curr[1]]
    if d == 'L':
        curr[0] -= 1
    elif d == 'R':
        curr[0] += 1
    elif d == 'U':
        curr[1] += 1
    else:
        assert d == 'D'
        curr[1] -= 1
    return curr
        
def diff(t1, t2):
    return sum([abs(t1[0] - t2[0]), abs(t1[1] - t2[1])])
    
def update_tail(head, tail):
    a = head == tail
    b = diff(head, tail) == 1 
    c = (abs(tail[0] - head[0]) == 1) and (abs(tail[1] - head[1]) == 1)
    if a or b or c:
        return tail
    elif head[0] == tail[0]:
        assert abs(head[1] - tail[1]) == 2
        return [tail[0], int((tail[1] + head[1])/2)]
    elif head[1] == tail[1]:
        assert abs(head[0] - tail[0]) == 2
        return [int((tail[0] + head[0])/2), tail[1]]
    else:
        option_1 = [tail[0]+1, tail[1]+1]
        option_2 = [tail[0]-1, tail[1]+1]
        option_3 = [tail[0]+1, tail[1]-1]
        option_4 = [tail[0]-1, tail[1]-1]
        options = [option_1, option_2, option_3, option_4]
        smallest_d = 1000
        best_o = -1
        for o in options:
            if diff(o, head) < smallest_d:
                best_o = o
                smallest_d = diff(o, head)
        return best_o
        
    

def fn_1(x):
    places = set()
    s = [0, 0]
    h = [0, 0]
    t = [0, 0]
    places.add(str(t))
    for move in x:
        d, m = move.split(' ')
        for i in range(int(m)):           
            h = update_head(h, d)
            t = update_tail(h, t)
            places.add(str(t))
    return len(places)

print(fn_1(x))


def update_tail_2(head, tail):
    a = head == tail
    b = diff(head, tail) == 1 
    c = (abs(tail[0] - head[0]) == 1) and (abs(tail[1] - head[1]) == 1)
    if a or b or c:
        return tail
    elif head[0] == tail[0]:
        if head[1] > tail[1]:
            return [tail[0], int(tail[1]+1)]
        else:
            return [tail[0], int(tail[1]-1)]
    elif head[1] == tail[1]:
        if head[0] > tail[0]:
            return [int(tail[0]+1), tail[1]]
        else:
            return [int(tail[0]-1), tail[1]]            
    else:
        option_1 = [tail[0]+1, tail[1]+1]
        option_2 = [tail[0]-1, tail[1]+1]
        option_3 = [tail[0]+1, tail[1]-1]
        option_4 = [tail[0]-1, tail[1]-1]
        options = [option_1, option_2, option_3, option_4]
        smallest_d = 1000
        best_o = -1
        for o in options:
            if diff(o, head) < smallest_d:
                best_o = o
                smallest_d = diff(o, head)
        return best_o
        
    
def fn_2(x):
    places = set()
    knots = [[0,0] for i in range(10)]
    places.add(str(knots[-1]))
    for move in x:
        d, m = move.split(' ')
        for k in range(int(m)):           
            h = update_head(knots[0], d)
            knots[0] = h
            for i in range(1, 10):
                t = update_tail_2(knots[i-1], knots[i])
                knots[i] = t
            places.add(str(t))
    return len(places)


print(fn_2(x))