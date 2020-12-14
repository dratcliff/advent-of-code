from timeit import default_timer as timer

def timed(f):
    def t(*args, **kwargs):
        start = timer()
        result = f(*args, **kwargs)
        end = timer()
        print(f.__name__, "took", (end-start)*1000, "ms")
        return result
    return t

def file_to_int_list(filename):
    entries = []
    with open(filename, "r") as f:
        for line in f:
            entries.append(int(line))
    return entries

def file_to_string_list(filename):
    entries = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip('\n')
            entries.append(line)
    return entries

def file_to_grid(filename):
    grid = {}
    with open(filename) as f:
        cur_line = 0
        for line in f:
            line = line.strip('\n')
            if cur_line not in grid:
                grid[cur_line] = {}
            for i, pt in enumerate(line):
                grid[cur_line][i] = pt
            cur_line += 1
    return grid

from collections import deque
def bfs(graph, vertex):
    queue = deque([vertex])
    level = {vertex: 0}
    parent = {vertex: None}
    while queue:
        v = queue.popleft()
        for n in graph[v]:
            if n not in level:            
                queue.append(n)
                level[n] = level[v] + 1
                parent[n] = v
    return level, parent

def bfs_example():
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'D'],
        'D': ['B', 'C', 'E'],
        'E': ['B', 'D']
    }
    level, parent = bfs(graph, 'A')
    print(level, parent)

def dfs(graph, vertex):
    parents = {vertex: None}
    dfs_visit(graph, vertex, parents)
    return parents

def dfs_visit(graph, vertex, parents):
    for n in graph[vertex]:
        if n not in parents:
            parents[n] = vertex
            dfs_visit(graph, n, parents)

def dfs_example():
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'D'],
        'D': ['B', 'C', 'E'],
        'E': ['B', 'D']
    }
    parents = dfs(graph, 'A')
    print(parents)

def dp_example():
    fs = {}
    def factorial(n):
        if n == 0:
            return 1
        elif n in fs:
            return fs[n]
        else:
            x = factorial(n-1) * n
            fs[n] = x
            return x
    print(factorial(500))
    

