xs = [x.strip("\n") for x in open("input.txt", "r").readlines()]

G = {}
X_DIM = len(xs[0])
Y_DIM = len(xs)

for y in range(len(xs)):
    for x in range(len(xs[y])):
        G[(x, y)] = xs[y][x]


def render(grid, x, y):
    s = ""
    for _y in range(y):
        for _x in range(x):
            s += grid[(_x, _y)]
        s += "\n"
    print(s)


# render(G, X_DIM, Y_DIM)

from collections import namedtuple

something = {
    # right
    "R": {
        ".": [((1, 0), "R")],
        "/": [((0, -1), "U")],
        "\\": [((0, 1), "D")],
        "-": [((1, 0), "R")],
        "|": [((0, 1), "D"), ((0, -1), "U")],
    },
    # left
    "L": {
        ".": [((-1, 0), "L")],
        "/": [((0, 1), "D")],
        "\\": [((0, -1), "U")],
        "-": [((-1, 0), "L")],
        "|": [((0, 1), "D"), ((0, -1), "U")],
    },
    # up
    "U": {
        ".": [((0, -1), "U")],
        "/": [((1, 0), "R")],
        "\\": [((-1, 0), "L")],
        "-": [((1, 0), "R"), ((-1, 0), "L")],
        "|": [((0, -1), "U")],
    },
    # down
    "D": {
        ".": [((0, 1), "D")],
        "/": [((-1, 0), "L")],
        "\\": [((1, 0), "R")],
        "-": [((1, 0), "R"), ((-1, 0), "L")],
        "|": [((0, 1), "D")],
    },
}
m = -1
start = []
for _x in range (0, X_DIM):
    for _y in range(0, Y_DIM):
        if _x == 0:
            start.append(((_x, _y), 'R'))
        if _y == 0:
            start.append(((_x,_y), 'D'))
        if _x == X_DIM-1:
            start.append(((_x,_y),'L'))
        if _y == Y_DIM-1:
            start.append(((_x,_y), 'U'))

for s in start:
    visited = set()
    paths = set()
    beams = []
    beams.append((s[0], s[1]))
    while beams:
        next_beams = []
        for pt, dir in beams:
            if (pt, dir) in paths:
                continue
            visited.add(pt)
            paths.add((pt,dir))
            cur_shape = G[pt]
            dx = something[dir][cur_shape]
            for o, d in dx:
                no = (pt[0]+o[0], pt[1]+o[1])
                if 0 <= no[0] < X_DIM and 0 <= no[1] < Y_DIM:
                    next_beams.append((no, d))
        beams = next_beams
    if len(visited) > m:
        m = len(visited)
    print(m,s)