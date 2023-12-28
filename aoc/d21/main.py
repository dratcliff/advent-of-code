xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]

G = {}
S = None
for y in range(len(xs)):
    for x in range(len(xs[y])):
        G[(x,y)] = xs[y][x]
        if G[(x,y)] == 'S':
            S = (x,y)
            G[(x,y)] = '.'

print(S)

at = set()
at.add(S)


from collections import deque

for i in range(640):
    Q = deque()
    Q.extend(at)
    at = set()
    while Q:
        cur = Q.popleft()
        for D in [(0,1),(0,-1),(1,0),(-1,0)]:
            nxt = (cur[0]+D[0],cur[1]+D[1])
            if nxt in G and G[nxt] == '.':
                at.add(nxt)
    print(i, len(at))