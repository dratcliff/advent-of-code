from collections import defaultdict


def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()


lines = get_data('input.txt')
lines = lines.strip().split('\n')

grid = {}

for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        if lines[y][x] == "#":
            grid[(x, y)] = lines[y][x]


def render():
    miny = min(grid.keys(), key=lambda x: x[1])[1]
    maxy = max(grid.keys(), key=lambda x: x[1])[1]
    minx = min(grid.keys(), key=lambda x: x[0])[0]
    maxx = max(grid.keys(), key=lambda x: x[0])[0]
    s = ""
    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            p = "#" if (x, y) in grid else "."
            s += p
        s += '\n'
    # print(s)
    return s.count(".")


N = (0, -1)
NE = (1, -1)
NW = (-1, -1)

S = (0, 1)
SE = (1, 1)
SW = (-1, 1)

W = (-1, 0)
E = (1, 0)

D8 = [N, NE, E, SE, S, SW, W, NW]

MOVES = [
    [N, NE, NW],
    [S, SE, SW],
    [W, NW, SW],
    [E, NE, SE]
]
moved = True
i = 0
while moved:
    moved = False
    c = defaultdict(list)
    for k in grid.keys():
        should_move = False
        for d in D8:
            if (k[0]+d[0], k[1]+d[1]) in grid:
                should_move = True
                break
        if not should_move:
            continue
        else:
            moved = True
        for m in range(0, 4):
            can_move = True
            moves = MOVES[(i+m) % 4]
            for move in moves:
                if (k[0]+move[0], k[1]+move[1]) in grid:
                    can_move = False
                    break
            if can_move:
                dest = (k[0]+moves[0][0], k[1]+moves[0][1])
                c[dest].append(k)
                break
    for k, v in c.items():
        if len(v) != 1:
            continue
        src = v[0]
        dest = k
        grid.pop(src)
        grid[k] = "#"
    i += 1
    if i == 10:
        print("part one", render())

print("part two", i)
