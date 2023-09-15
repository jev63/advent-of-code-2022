from utils import read_input, read_test
from collections import defaultdict

x = read_input(5)


def pre(x):
    IDX_OF_INTEREST = [1, 5, 9, 13, 17, 21, 25, 29, 33]
    LAST_IDX = 7
    INSTRUCTION_START = 10
    d = defaultdict(list)
    
    for row in x[:LAST_IDX+1]:
        for i, idx in enumerate(IDX_OF_INTEREST, 1):
            if row[idx] not in ('[', ']', ' '):
                d[i].insert(0,row[idx])
    m = []            
    for row in x[INSTRUCTION_START:]:
        row = row.split(' ')
        m.append((int(row[1]), int(row[3]), int(row[5])))
        
    return d, m


def fn_1(x):
    board, moves = pre(x)
    for n, a, b in moves:
        for i in range(n):
            board[b].append(board[a].pop())
    out = ''
    for i in range(1, 10):
        out += board[i][-1]
    return out
            
            
print(fn_1(x))


def fn_2(x):
    board, moves = pre(x)
    for n, a, b in moves:
            board[b].extend(board[a][-n:])
            board[a] = board[a][:-n]
    out = ''
    for i in range(1, 10):
        out += board[i][-1]
    return out
        
    
print(fn_2(x))