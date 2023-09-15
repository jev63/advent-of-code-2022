def read_input(day):
    with open(f'./aoc/input_{day}.txt', 'r') as f:
        x = [s.strip() for s in f.readlines()]
    return x

def read_test(day):
    with open(f'./aoc/input_{day}_test.txt', 'r') as f:
        x = [s.strip() for s in f.readlines()]
    return x