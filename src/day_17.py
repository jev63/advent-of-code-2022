from utils import read_input, read_test
import math
import numpy as np

x = read_input(17)
x_ = read_test(17)


class Chamber:
    
    def minus_handler_(chamber):
        idxs = [(3,2), (3,3), (3,4), (3,5)]
        for idx in idxs:
            chamber[idx] = 2
        return idxs
        
    def plus_handler_(chamber):
        idxs = [(2,2), (2,3), (2,4), (1,3), (2,3), (3,3)]
        for idx in idxs:
            chamber[idx] = 2
        return idxs

    def ell_handler_(chamber):
        idxs = [(3,2), (3,3), (3,4), (1,4), (2,4), (3,4)]
        for idx in idxs:
            chamber[idx] = 2
        return idxs
        
    def stick_handler_(chamber):
        idxs = [(0,2), (1,2), (2,2), (3,2)]
        for idx in idxs:
            chamber[idx] = 2
        return idxs
       
    def square_handler_(chamber):
        idxs = [(2,2), (2,3), (3,2), (3,3)]
        for idx in idxs:
            chamber[idx] = 2
        return idxs
        
    def __repr__(self):
        r = ''
        for row in self.chamber:
            r += ''.join(['.' if elt == 0 else '@' if elt == 2 else '#' for elt in row]) + '\n'
        return r
    
    HANDLERS = {
        '-': minus_handler_,
        '+': plus_handler_,
        'L': ell_handler_,
        '|': stick_handler_,
        'o': square_handler_,   
    }
    
    def __init__(self, rock, bottom):
        self.chamber = np.zeros((7,7))
        self.idxs = self.place_rock(rock)
        self.attach_bottom(bottom)

        
    def place_rock(self, rock):
        return Chamber.HANDLERS[rock](self.chamber)
        
    def attach_bottom(self, bottom):
        self.chamber = np.concatenate((self.chamber, bottom))
        
    def fix(self):
        self.chamber[self.chamber==2] = 1
    
    def simulate(self, direction):
        if direction == '<':
            stuck = self.move_horizontal(-1)
        elif direction == '>':
            stuck = self.move_horizontal(+1)
        elif direction == 'v':
            stuck = self.move_down()
        return stuck
    
    def move_horizontal(self, direction):
        stuck = False
        for r, c in self.idxs:
            entry = self.chamber[r, c]
            stuck_left = ((c == 0) and (direction==-1))
            stuck_right = ((c == 6) and (direction==1))
            if stuck_left or stuck_right or (self.chamber[r,c+direction] == 1):
                stuck = True
                


        new_idxs = [(r, c+direction) for r, c in self.idxs]
        if not stuck:
            for r, c in new_idxs:
                self.chamber[r, c] = 2
                if (r, c-direction) not in new_idxs:
                    self.chamber[r,c-direction] = 0
                
            self.idxs = new_idxs
            
        return stuck
    
    def move_down(self):
        stuck = False
        for r, c in self.idxs:
            entry = self.chamber[r, c]
            
            if (r == len(self.chamber)-1) or (self.chamber[r+1,c] == 1):
                stuck = True

        new_idxs = [(r+1, c) for r, c in self.idxs]
        if not stuck:
            for r, c in new_idxs:
                self.chamber[r, c] = 2
                if (r-1, c) not in new_idxs:
                    self.chamber[r-1,c] = 0
                
            self.idxs = new_idxs
            
        return stuck
    
    @property
    def top(self):
        for i, row in enumerate(self.chamber):
            if any(row == 1):
                return i
        
def pre(x):
    return x[0]


def fn_1(x):
    x = pre(x)
    order = ['-', '+', 'L', '|', 'o']
    bottom = np.ones((1,7))
    i = 0
    for n in range(N):
        rock = order[n%len(order)]
        chamber = Chamber(rock, bottom)
        
        fallen = False
        while not fallen:
            direction = x[i%len(x)]
            chamber.simulate(direction)
            fallen = chamber.simulate('v')
            i+=1
        chamber.fix()
        bottom = chamber.chamber[chamber.top:]

    return len(chamber.chamber) - (chamber.top+1)
        

N = 2022
print(fn_1(x))
    
def residual_simulation(x, N):
    order = ['|', 'o', '-', '+', 'L',]

    
    bottom = np.array([
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0],
        [1, 1, 1, 0, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 0],
    ]
    )
    i=0
    for n in range(N):
        rock = order[n%len(order)]
        chamber = Chamber(rock, bottom)

        fallen = False
        while not fallen:
            direction = x[i%len(x)]
            chamber.simulate(direction)
            fallen = chamber.simulate('v') 
            i+=1
        chamber.fix()
        bottom = chamber.chamber[chamber.top:]

    return len(chamber.chamber)-9-(chamber.top)
    

def fn_2(x):
    x = pre(x)
    n_fallen_per_period = 1735
    height_after_period = 2720
    sim_len = 1000000000000
    n_periods = math.floor(sim_len / n_fallen_per_period)
    residual_n_turns = sim_len - (n_periods*n_fallen_per_period)
    
    residual_height = residual_simulation(x, 140)
    out = (n_periods*height_after_period)+residual_height
    return out
    
print(fn_2(x))