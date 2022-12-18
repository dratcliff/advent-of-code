from itertools import combinations
from collections import deque, defaultdict


def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()


lines = get_data('input.txt')
lines = lines.strip().split('\n')
lines = [x.split(',') for x in lines]
lines = [tuple(int(x) for x in y) for y in lines]


def adjacent(t1, t2):
    if abs(t1[0]-t2[0]) > 1 or abs(t1[1]-t2[1]) > 1 or abs(t1[2]-t2[2]) > 1:
        return False
    c = abs(t1[0]-t2[0]) + abs(t1[1]-t2[1]) + abs(t1[2]-t2[2])
    return c == 1


total = 6 * len(lines)


# not terribly helpful for part two :(
for c in combinations(lines, 2):
    if adjacent(c[0], c[1]):
        total -= 2

print("Part one:", total)

mx = max(lines, key=lambda x: x[0])[0]+1
my = max(lines, key=lambda x: x[1])[1]+1
mz = max(lines, key=lambda x: x[2])[2]+1
upper = (mx, my, mz)
mnx = min(lines, key=lambda x: x[0])[0]-1
mny = min(lines, key=lambda x: x[1])[1]-1
mnz = min(lines, key=lambda x: x[2])[2]-1
lower = (mnx, mny, mnz)
lava = set(lines)

ds = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


ext = defaultdict(int)
seen = set()


Q = deque()
Q.append((mx, my, mz))

# could've been recursive? wasn't sure about python's depth limit
while Q:
    pt = Q.popleft()
    if pt in seen:
        continue
    seen.add(pt)
    for d in ds:
        nxt = (pt[0]+d[0], pt[1]+d[1], pt[2]+d[2])
        # one direction is lava == one exterior face
        if (nxt) in lava:
            ext[pt] += 1
        else:
            if all([x[0] <= x[1] for x in zip(nxt, upper)]) and all([x[0] >= x[1] for x in zip(nxt, lower)]):
                Q.append(nxt)

print("Part two:", sum(ext.values()))
