from utils import read_input, read_test
from dataclasses import dataclass
from typing import Any
import copy

x = read_input(16)
x_ = read_test(16)


def shrink(graph, keep=None, special=None):
    for nname in graph:
        node = graph[nname]
        if node.rate == 0 and len(node.edges) == 2:
            e1, e2 = [graph[e] for e in node.edges]

            e1_dist = e1.edges[nname]
            e2_dist = e2.edges[nname]
            del e1.edges[nname]
            del e2.edges[nname]
            
            bridge_dist = e1_dist + e2_dist
            
            if e2.name not in e1.edges:
                assert e1.name not in e2.edges
                e2.edges[e1.name] = bridge_dist
                e1.edges[e2.name] = bridge_dist
                
    keys = list(graph.keys())
    for k in keys:
        needed = False
        for v in graph.values():
            if k in v.edges:
                needed = True
        if not needed:
            del graph[k]
            
    if keep:
        new = {}
        for k, v in list(graph.items()):
            if k in keep:
                if k == special:
                    for thing in list(v.edges):
                        if thing not in keep:
                            del v.edges[thing]
                new[k] = v
        graph = new
                    
    return graph


@dataclass
class Valve:
    def __init__(self, name, rate, edges, wait=1):
        self.name = name
        self.rate = rate
        self.edges = edges
        self.pressure = 0
        self._released = 0
        self.wait_time = wait
        
    @property
    def released(self):
        return self._released
    
    @released.setter
    def released(self, r):
        self._released=r
    

def pre(x):
    valves = {}
    for valve in x:
        valve = valve.split(' ')
        name = valve[1]
        rate = int(valve[4].split('=')[-1][:-1])
        edges = valve[9:]
        edges = {e.split(',')[0]: 1 for e in edges}
        valves[name] = Valve(name, rate, edges)
    
    return valves

        
def get_pressure(chain):
    s = 0
    for x in chain:
        if '=' in x:
            s_ = int(x.split('=')[-1])
            s += s_
    return s
        

def dfs(valve, nodes, time, release, chain, chain_, chain__):
    chain.append(f'{valve.name} ({release})')
    chain_.append(valve.name)
    chain__.add('-'.join([valve.name, str(release)]))
    total_pressure = get_pressure(chain)
    options = []    

        
    if time <= 1:
        chain.pop(-1)
        chain_.pop(-1)
        chain__ -= set(['-'.join([valve.name, str(release)])])
        return total_pressure
    
    # consider switching these blocks
    if release:
        time-=1
        chain[-1] += f'{valve.rate}x{time}={valve.rate*time}'
        total_pressure = get_pressure(chain)
        if time in {0, 1}:
            chain.pop(-1)
            chain_.pop(-1)
            chain__ -= set(['-'.join([valve.name, str(release)])])
            return total_pressure
    

    if time > 1:
        for v, wait in valve.edges.items():
            v = nodes[v]
            if ok(chain_, valve.name, v.name):
                if f'{v.name}-True' not in chain__ and v.rate > 0:
                    options.append(dfs(v, nodes, time-wait, True, chain, chain_, chain__))
                if v.rate < 5 or ((v.rate >= 5) and (f'{v.name}-True' in chain__)):
                    options.append(dfs(v, nodes, time-wait, False, chain, chain_, chain__))
        

        if options:

            chain.pop(-1)
            chain_.pop(-1)
            chain__ -= set(['-'.join([valve.name, str(release)])])
            return max(options)
        else:
            chain.pop(-1)
            chain_.pop(-1)
            chain__ -= set(['-'.join([valve.name, str(release)])])
            return total_pressure
            
    
    
def ok(chain, current_v, next_v):
    p1 = [current_v, next_v, current_v]
    p2 = [current_v, next_v, '???', next_v, current_v]
    if chain[-3:] == p1:
        return False
    elif chain[-5:-3] + ['???'] + chain[-2:] == p2:
        return False
    else:
        return True


def fn_1(x):
    x = shrink(pre(x))
    return dfs(x['AA'], x, 30, False, [], [], set())
    
print(fn_1(x))

@dataclass
class Action:
    graph: Any
    name: str  # this is the payers name
    current_node: str
    current_action: bool
    next_node: str
    next_action: bool
    #history: list
    time: int
    time_to_next_node: int
    start: list
        
    def __repr__(self):
        return f'({self.name}, {self.current_node}({self.time_to_next_node}), {self.current_action}, {self.time})'



@dataclass
class Player:
    graph: Any
    name: str
    current_node: str
    current_action: bool
    next_node: str
    next_action: bool
    start: list
        
    def __post_init__(self):
        self.time_to_next_node=1
        self.time=TIME
        snapshot = copy.deepcopy(self.__dict__)
        self.history=[Action(**snapshot)]
         
    def step(self):
        self.time-=1
        self.time_to_next_node-=1
        # act
        self.current_node = self.next_node
        self.current_action = self.next_action
        self.next_node = None
        self.next_action = None
        snapshot = copy.deepcopy(self.__dict__)
        del snapshot['history']
        self.history.append(Action(**snapshot))  # maybe indicate transit   
        
    def pop(self):
        self.history.pop(-1)
        previous_snapshot = copy.deepcopy(self.history[-1].__dict__)
        self.__dict__.update(previous_snapshot)
        
    def set_next(self, next_node, next_action):
        if self.arrived():
            self.next_node = next_node
            self.next_action = next_action
            if self.next_action:  # case where waiting at current node to release valve
                self.time_to_next_node = 1 + self.graph[next_node].edges[self.current_node]
            else:
                self.time_to_next_node = self.graph[next_node].edges[self.current_node]
        else:
            self.next_node = self.current_node
            self.next_action = self.current_action
            
    def arrived(self):
        return self.time_to_next_node == 0
        
        
    @property
    def neighbors(self):
        if not self.arrived():
            # means you havent arrived there yet
            rval = [self.current_node]
        else:
            chain = [self.history[1].current_node]
            for act in self.history[1:]:
                node = act.current_node
                if chain[-1] != node:
                    chain.append(node)
            if self.start and len(chain) < len(self.start):
                n_so_far = len(chain)
                assert self.start[:n_so_far] == chain
                rval = [self.start[n_so_far]]
            else:
                rval = reversed(self.graph[self.current_node].edges.keys())
                rval = [n for n in rval if self.ok(n)]
            
        return rval
            

    def ok(self, next_node):
        if next_node in SKIP:
            return False

        chain = [self.history[1].current_node]
        for act in self.history[1:]:
            node = act.current_node
            if chain[-1] != node:
                chain.append(node)
                
        current_node = self.history[-1].current_node
        pattern_1 = [current_node, next_node, current_node]
        pattern_2 = [current_node, next_node, '???', next_node, current_node]
               
        if chain[-3:] == pattern_1:
            return False
        elif chain[-5:-3] + ['???'] + chain[-2:] == pattern_2:
            return False
        else:
            return True


        
    @property
    def active_history(self):
        return [a.current_node for a in self.history if a.current_action]
    
    def __repr__(self):
        strs = []
        for action in self.history[1:]:
            strs.append(action.__repr__())
        return ' --> '.join(strs)
    

def get_actions(p1, p2, n1, n2):
    p1_n1_actions = []
    p2_n2_actions = []
    if not p1.arrived():
        p1_n1_actions+=[p1.current_action]
    else:
        if (n1 not in p1.active_history) and (n1 not in p2.active_history) and p1.graph[n1].rate > 0:
            p1_n1_actions+=[True]
        if (p1.graph[n1].rate < 5) or ((p1.graph[n1].rate >=5) and (n1 in p1.active_history) or (n1 in p2.active_history)):
            p1_n1_actions+=[False]
        
    if not p2.arrived():
        p2_n2_actions+=[p2.current_action]
    else:
        if (n2 not in p1.active_history) and (n2 not in p2.active_history) and (p1.graph[n2].rate > 0): #and (n1 != n2):
            p2_n2_actions+=[True]
        if (p2.graph[n2].rate < 5) or ((p2.graph[n2].rate >=5)  and (n2 in p1.active_history) or (n2 in p2.active_history)):
            p2_n2_actions+=[False]
        
    out = []
    for a1 in p1_n1_actions:
        for a2 in p2_n2_actions:
            out.append((a1, a2))

    return out


def score(p1, p2):
    s_p1 = sum(a.time * p1.graph[a.current_node].rate for a in p1.history if a.current_action and a.time_to_next_node==0)
    s_p2 = sum(a.time * p1.graph[a.current_node].rate for a in p2.history if a.current_action and a.time_to_next_node==0)

    return s_p1 + s_p2


def check(p, match):
    nodes = [a.current_node for a in p.history[1:]]
    match = [f'{x}{x}' for x in match]
    if match == nodes:
        import pdb; pdb.set_trace()


def dfs_2(p1, p2):
    assert p2.time == p1.time
    p1.step()
    p2.step()
    if p1.time in {0, 1}:
        s = score(p1, p2)
        p1.pop()
        p2.pop()
        return s
    else:
        options = []
        for n1 in p1.neighbors:
            for n2 in p2.neighbors:
                for a1, a2 in get_actions(p1, p2, n1, n2):
                    p1.set_next(n1, a1)
                    p2.set_next(n2, a2)
                    options.append(dfs_2(p1, p2))
        
        p1.pop()
        p2.pop()
        return max(options)

TIME=27
SKIP={'AA'}

def fn_2(x):
    x = shrink(pre(x))
    p1 = Player(x, 'Me', None, False, 'AA', False, start=['AA', 'UV', 'FC', 'EZ', 'OY'])
    p2 = Player(x, 'El', None, False, 'AA', False, start=['AA', 'TO', 'JT', 'KE', 'IR', 'PH', 'IF', 'IR', 'SV'])
    return dfs_2(p1, p2)


print(fn_2(x))
        
