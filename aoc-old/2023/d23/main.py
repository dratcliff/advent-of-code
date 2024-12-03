from collections import deque
xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]

X_DIM = len(xs[0])
Y_DIM = len(xs)

G = {}
S = None
E = None
for y in range(Y_DIM):
    for x in range(X_DIM):
        if y == 0 and xs[y][x] == '.':
            assert S == None
            S = (x, y)
        if y == Y_DIM-1 and xs[y][x] == '.':
            assert E == None
            E = (x, y)
        G[(x, y)] = xs[y][x]

assert S != None
assert E != None

slopes = {
    '>': (1, 0),
    '<': (-1, 0),
    'v': (0, 1),
    '^': (0, -1)
}

Q = deque()
Q.append((S, ((),)))
longest = 0
while Q:
    cur, visited = Q.popleft()
    # print(cur, visited)
    if cur not in visited:
        assert G[cur] != '#'
        visited = visited + (cur,)
        if cur == E:
            l = len(visited)-2
            if l > longest:
                longest = l
        elif G[cur] == '.':
            for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nxt = (cur[0]+d[0], cur[1]+d[1])
                if nxt in G and G[nxt] != '#':
                    Q.append((nxt, visited))
        else:
            d = slopes[G[cur]]
            nxt = (cur[0]+d[0], cur[1]+d[1])
            if nxt in G and G[nxt] == '.':
                Q.append((nxt, visited))

print(longest)

# p2

M = {}


def next_nodes(start, last, distance=0):
    if (start, last) in M:
        return M[(start, last)]
    dist = distance
    nodes = []
    for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nxt = (start[0]+d[0], start[1]+d[1])
        if nxt != last and nxt in G and G[nxt] != '#':
            nodes.append((1, nxt))
    if len(nodes) != 1 and distance > 0:
        v = [(distance, start)]
        M[(start, last)] = v
        return [(distance, start)]
    if len(nodes) > 1 or len(nodes) == 0:
        M[(start, last)] = nodes
        return nodes
    else:
        assert len(nodes) == 1
        cur_nxt = nodes[0][1]
        v = next_nodes(cur_nxt, start, dist+1)
        M[(start, last)] = v
        return v


Q = deque()
Q.append((0, S, ((),)))
L = 0
while Q:
    dist, cur, visited = Q.pop()
    if cur not in visited:
        nxt = next_nodes(cur, visited[-1])
        for d, pt in nxt:
            if pt == E:
                if dist+d > L:
                    L = d+dist
            else:
                if pt not in visited:
                    Q.append((dist+d, pt, visited + (cur,)))

print(L)  # takes a minute
