from utils import read_input, read_test

x = read_input(2)

class Rock:
    def __init__(self):
        self.value = 1
        self.loses_to = Paper
        self.beats = Scizzor

    def __gt__(self, other):
        if isinstance(other, Scizzor):
            return True
        else:
            return False
        
    def __eq__(self, other):
        if isinstance(other, Rock):
            return True
        else:
            return False
        
class Paper:
    def __init__(self):
        self.value = 2
        self.loses_to = Scizzor
        self.beats = Rock

    def __gt__(self, other):
        if isinstance(other, Rock):
            return True
        else:
            return False
        
    def __eq__(self, other):
        if isinstance(other, Paper):
            return True
        else:
            return False
        
class Scizzor:
    def __init__(self):
        self.value = 3
        self.loses_to = Rock
        self.beats = Paper

    def __gt__(self, other):
        if isinstance(other, Paper):
            return True
        else:
            return False
        
    def __eq__(self, other):
        if isinstance(other, Scizzor):
            return True
        else:
            return False
        
def play_1(x):
    if x in ('A', 'X'):
        return Rock()
    elif x in ('B', 'Y'):
        return Paper()
    else:
        return Scizzor()
        
def score(you, other):
    WIN = 6
    TIE = 3
    LOSS = 0
    if you > other:
        return WIN + you.value
    elif you == other:
        return TIE + you.value
    else:
        return you.value

def fn_1(x):
    s = 0
    for y in x:
        other, you = y.split(' ')
        other, you = play_1(other), play_1(you)
        s += score(you, other)
    return s

print(fn_1(x))


def play_2(x):
    if x == 'A':
        return Rock()
    elif x == 'B':
        return Paper()
    else:
        return Scizzor()
    
def your_play(you, other):
    if you == 'X':
        return play_2(other).beats()
    elif you == 'Y':
        return play_2(other)
    else:
        return play_2(other).loses_to()
    
    
    
    
    
def fn_2(x):
    s = 0
    for y in x:
        other, you = y.split(' ')
        you = your_play(you, other)
        other = play_2(other)
        z = score(you, other)
        s += z
    return s
        
    
print(fn_2(x))