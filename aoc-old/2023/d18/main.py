from collections import deque
xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
xs = [x.split()[:2] for x in xs]
xs = [(x[0], int(x[1])) for x in xs]
# print(xs)


def render(grid, xmin, xmax, ymin, ymax):
    s = ""
    for _y in range(ymin, ymax+1):
        for _x in range(xmin, xmax+1):
            pt = (_x, _y)
            if pt in grid:
                s += '#'
            else:
                s += '.'
        s += '\n'
    print(s)


xmin = 0
xmax = 0
ymin = 0
ymax = 0

G = {}
cur = (0, 0)

for dir, dist in xs:
    shift = None
    match dir:
        case 'R':
            shift = (1, 0)
        case 'L':
            shift = (-1, 0)
        case 'D':
            shift = (0, 1)
        case 'U':
            shift = (0, -1)
    for i in range(dist):
        cur = (cur[0]+shift[0], cur[1]+shift[1])
        G[cur] = '#'
        if cur[0] < xmin:
            xmin = cur[0]
        if cur[0] > xmax:
            xmax = cur[0]
        if cur[1] < ymin:
            ymin = cur[1]
        if cur[1] > ymax:
            ymax = cur[1]

top_corner = None
y = ymin
x = xmin-1
while not top_corner:
    pt = (x, y)
    rt = (x+1, y)
    dn = (x, y+1)
    if pt in G and rt in G and dn in G:
        top_corner = pt
    x += 1

ct = len(G.values())
seen = set()
Q = deque()
Q.append((top_corner[0]+1, top_corner[1]+1))

while Q:
    cur = Q.popleft()
    if cur not in seen and cur not in G:
        seen.add(cur)
        ct += 1
        for D in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nxt = (cur[0]+D[0], cur[1]+D[1])
            if nxt not in G:
                Q.append(nxt)

print(ct)
