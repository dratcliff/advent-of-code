from collections import defaultdict
from utilaoc import file_to_strings

actual = file_to_strings("a.txt")
actual = actual = [x.split(' ') for x in actual]
b = []
for a in actual:
    c = []
    c.append(a[0])
    d = a[1].split(',')
    d = [x.split('..') for x in d]
    for a in d:
        for z in a:
            c.append(z.replace("x", "").replace("y", "").replace("z", "").replace("=",""))
    b.append(c)

d = []
for a in b:
    e = []
    # print(a)
    e.append(a[0])
    e.append((min(int(a[1]), int(a[2])), max(int(a[1]), int(a[2]))))
    e.append((min(int(a[3]), int(a[4])), max(int(a[3]), int(a[4]))))
    e.append((min(int(a[5]), int(a[6])), max(int(a[5]), int(a[6]))))
    d.append(e)

def intersection(x1, x2, y1, y2, z1, z2, xa, xb, ya, yb, za, zb):
    leftx = max(x1, xa)
    rightx = min(x2, xb)

    lefty = max(y1, ya)
    righty = min(y2, yb)

    leftz = max(z1, za)
    rightz = min(z2, zb)
    if leftx >= rightx or lefty >= righty or leftz >= rightz:
        return None
    return (leftx, rightx, lefty, righty, leftz, rightz)

grid = defaultdict(int)
for ii in d:
    xyz = (ii[1][0], ii[1][1], ii[2][0],ii[2][1],ii[3][0],ii[3][1])
    for g, v in list(grid.items()):
        intersect = intersection(xyz[0], xyz[1], xyz[2], xyz[3], xyz[4], xyz[5],\
            g[0], g[1], g[2], g[3], g[4], g[5])
        if intersect != None:
            # h = intersect
            # dx = abs(h[1]-h[0])+1
            # dy = abs(h[3]-h[2])+1
            # dz = abs(h[5]-h[4])+1
            # vx = dx * dy * dz
            # print("-", vx)
            grid[intersect] -= v
    if ii[0] == 'on':
        # h = xyz
        # dx = abs(h[1]-h[0])+1
        # dy = abs(h[3]-h[2])+1
        # dz = abs(h[5]-h[4])+1
        # vx = dx * dy * dz
        # print("+", vx)
        grid[xyz] += 1
    
    
t = 0
for g, v in grid.items():
    # print(g)
    dx = abs(g[1]-g[0])+1
    dy = abs(g[3]-g[2])+1
    dz = abs(g[5]-g[4])+1
    v = dx * dy * dz * v
    t += v

# this looks nothing like what i did for part 1, but oh well
# for part one just remove the lines outside the range and it still works i think
print(t)