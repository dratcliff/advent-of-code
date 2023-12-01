def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()

lines = get_data('input.txt')
lines = lines.strip().split('\n')

from collections import defaultdict
grid = defaultdict(list)
grids = []
h = len(lines)
w = len(lines[0])

for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        if lines[y][x] != '.':
            grid[(x,y)].append(lines[y][x])

grids.append(grid)

def render(g):
    s = ""
    for y in range(0, h):
        for x in range(0, w):
            if len(g[(x,y)]) == 1:
                s += g[(x,y)][0]
            else:
                s += str(len(g[(x,y)]))
        s += '\n'
    print(s)


def advance():
    last = grids[-1]
    nxt = defaultdict(list)
    for k, v in last.items():
        if len(v) == 1 and v[0] == "#":
            nxt[k].append("#")
        else:
            for bliz in v:
                if bliz == ">":
                    if k[0] == w-2:
                        nxt[(1, k[1])].append(">")
                    else:
                        nxt[(k[0]+1, k[1])].append(">")
                elif bliz == "<":
                    if k[0] == 1:
                        nxt[(w-2, k[1])].append("<")
                    else:
                        nxt[(k[0]-1, k[1])].append("<")
                elif bliz ==  "^":
                    if k[1] == 1:
                        nxt[(k[0], h-2)].append("^")
                    else:
                        nxt[(k[0], k[1]-1)].append("^")
                elif bliz == "v":
                    if k[1] == h-2:
                        nxt[(k[0], 1)].append("v")
                    else:
                        nxt[(k[0], k[1]+1)].append("v")
    grids.append(nxt)

advance()

for i in range(0, 1000):
    advance()

from collections import deque

def go(start, dest, cur_t):
    Q = deque()
    Q.append((start, cur_t, (start,)))
    seen = set()
    while Q:
        pos, t, path = Q.popleft()
        if pos == dest:
            return t
        if (pos, t) not in seen:
            nxtg = grids[t+1]
            for d in [(1,0), (-1,0), (0,1), (0,-1), (0,0)]:
                nxtp = (pos[0]+d[0], pos[1]+d[1])
                if len(nxtg[nxtp]) == 0 and 0 <= nxtp[0] <= w and 0 <= nxtp[1] <= h:
                    Q.append((nxtp, t+1, path + (nxtp,)))
        seen.add((pos, t))

t = go((1,0), (w-2,h-1), 0)
print("part one", t)
t = go((w-2,h-1), (1,0), t)
print("going back", t)
t = go((1,0), (w-2,h-1), t)
print("part two", t)