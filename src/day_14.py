from utils import read_input, read_test
import numpy as np

x = read_input(14)
x_ = read_test(14)

def pre(x):
    xmax, xmin, ymax, ymin = 500, 500, 0, 0
    out = []
    for rock in x:
        segments = rock.split(' -> ')
        for i in range(0,len(segments)-1):
            s1 = segments[i]
            s2 = segments[i+1]
            a, b = [int(y) for y in s1.split(',')]
            c, d = [int(y) for y in s2.split(',')]
            if a < xmin:
                xmin = a
            if a > xmax:
                xmax = a
            if b < ymin:
                ymin = b
            if b > ymax:
                ymax = b
            if c < xmin:
                xmin = c
            if c > xmax:
                xmax = c
            if d < ymin:
                ymin = d
            if d > ymax:
                ymax = d
            out.append([(a, b), (c, d)])
            

    return out, (xmax, xmin, ymax, ymin)


class Board:
    def __init__(self, xmax, xmin, ymax, ymin):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.board = [[0]*(xmax+1) for _ in range(ymax+1)]
        
    def put_rock(self, row, col):
        self.board[row][col] = 1

        
    def put_sand(self, row, col):
        if self.board[row+1][col] == 0:
            self.put_sand(row+1, col)
        elif self.board[row+1][col] > 0:
            if self.board[row+1][col-1] == 0:
                self.put_sand(row+1, col-1)
            elif self.board[row+1][col+1] == 0:
                self.put_sand(row+1, col+1)
            else:
                self.board[row][col] = 2
                        
       
    @property
    def shape(self):
        return np.array(self.board).shape
    
    @classmethod
    def from_input(cls, x):
        x, dims = pre(x)
        board = cls(*dims)
        for [(a, b), (c, d)] in x:
            order_1 = -1 if c < a else 1
            order_2 = -1 if d < b else 1
            for i in range(a, c+order_1, order_1):
                for j in range(b, d+order_2, order_2):
                    board.put_rock(j, i)
        return board
    
    

class Board2:
    def __init__(self, xmax, xmin, ymax, ymin):
        ymax += 2
        floor_size = 1 + 2*ymax + 3
        xmin_ = int(500 - floor_size/2)
        xmax_ = int(500 + floor_size/2)
        self.xmin = min(xmin, xmin_)
        self.xmax = max(xmax, xmax_)
        self.ymin = ymin
        self.ymax = ymax
        self.board = [[0]*(self.xmax+1) for _ in range(self.ymax+1)]
        
    def put_rock(self, row, col):
        self.board[row][col] = 1
        
    def put_sand(self, row, col):
        if self.board[row+1][col] == 0:
            self.put_sand(row+1, col)
        elif self.board[row+1][col] > 0:
            if self.board[row+1][col-1] == 0:
                self.put_sand(row+1, col-1)
            elif self.board[row+1][col+1] == 0:
                self.put_sand(row+1, col+1)
            else:
                self.board[row][col] = 2
                 
    @property
    def shape(self):
        return np.array(self.board).shape

    @classmethod
    def from_input(cls, x):
        x, dims = pre(x)
        board = cls(*dims)
        for [(a, b), (c, d)] in x:
            order_1 = -1 if c < a else 1
            order_2 = -1 if d < b else 1
            for i in range(a, c+order_1, order_1):
                for j in range(b, d+order_2, order_2):
                    board.put_rock(j, i)
        for i in range(len(board.board[0])):
            board.board[-1][i] = 1
        return board



def fn_1(x):
    board = Board.from_input(x)
                
    n = 0
    go = True
    while go and n < 10000:
        try:
            board.put_sand(0, 500)
            n += 1
        except Exception as e:
            go = False
    return n
        

print(fn_1(x))


def fn_2(x):
    board = Board2.from_input(x)
    
    n = 0
    while board.board[0][500] == 0:
        board.put_sand(0,500)
        n+=1
        
    return n
    
print(fn_2(x))
