import z3
from itertools import combinations
import math
xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
xs = [x.split(' @ ') for x in xs]
xs = [(x[0].split(', '), x[1].split(', ')) for x in xs]
xs = [(tuple([int(y) for y in x[0]]), tuple([int(y) for y in x[1]]))
      for x in xs]
xs = [(x[0][0], x[0][1], x[1][0], x[1][1]) for x in xs]


def get_eq(x, y, dx, dy):
    m = (dy/dx)
    b = y - m*x
    return (m, b)


def in_future(start_pos, vel, intersection):
    if not intersection:
        return False
    x1, y1 = start_pos
    x2, y2 = intersection
    dx, dy = vel
    xsign = math.copysign(1, x2-x1)
    ysign = math.copysign(1, y2-y1)
    xvsign = math.copysign(1, dx)
    yvsign = math.copysign(1, dy)
    return xsign == xvsign and ysign == yvsign


def lines_intersect_in_range(m1, b1, m2, b2, x_range, y_range):
    # Calculate the x-coordinate of the intersection point
    if m1 == m2:
        return None
    x_intersection = (b2 - b1) / (m1 - m2)
    # Check if the intersection point is within the specified x range
    if x_range[0] <= x_intersection <= x_range[1]:
        # Calculate the corresponding y-coordinate
        y_intersection = m1 * x_intersection + b1
        # Check if the y-coordinate is within the specified y range
        if y_range[0] <= y_intersection <= y_range[1]:
            return x_intersection, y_intersection
        else:
            return None
    else:
        return None


x_range = (200000000000000, 400000000000000)
y_range = x_range

ct = 0
for j, k in combinations(xs, 2):
    x1, y1, dx1, dy1 = j
    x2, y2, dx2, dy2 = k
    m1, b1 = get_eq(x1, y1, dx1, dy1)
    m2, b2 = get_eq(x2, y2, dx2, dy2)
    intersection = lines_intersect_in_range(m1, b1, m2, b2, x_range, y_range)
    if intersection and intersection and in_future((x1, y1), (dx1, dy1), intersection) and in_future((x2, y2), (dx2, dy2), intersection):
        ct += 1

print(ct)

xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
xs = [x.split(' @ ') for x in xs]
xs = [(x[0].split(', '), x[1].split(', ')) for x in xs]
xs = [(tuple([int(y) for y in x[0]]), tuple([int(y) for y in x[1]]))
      for x in xs]


def I(name): return z3.Real(name)


x, y, z = I('x'), I('y'), I('z')
vx, vy, vz = I('vx'), I('vy'), I('vz')

# no, I don't really know how to use z3
# but, yes, I was at least aware it existed lol

s = z3.Solver()

for i, j in enumerate(xs):
    (x1, y1, z1), (dx1, dy1, dz1) = j
    t = I(f't_{i}')
    s.add(t >= 0)
    s.add(x + vx * t == x1 + dx1*t)
    s.add(y + vy * t == y1 + dy1*t)
    s.add(z + vz * t == z1 + dz1*t)

assert s.check() == z3.sat

m = s.model()
x, y, z = m.eval(x), m.eval(y), m.eval(z)
x, y, z = x.as_long(), y.as_long(), z.as_long()

print(x+y+z)
