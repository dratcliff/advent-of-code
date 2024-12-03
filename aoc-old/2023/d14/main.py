def render(x, y, Os, Hs):
    s = ""
    for _y in range(y):
        for _x in range(x):
            v = "O" if (_x, _y) in Os else "#" if (_x, _y) in Hs else "."
            s += v
        s += "\n"
    print(s)


from collections import deque


def advance(o, h, at_limit_f, next_f, sort_f, desc):
    new_so = set()
    so = sorted(o, key=sort_f, reverse=desc)
    for o in so:
        above = next_f(o)
        while not at_limit_f(above) and above not in new_so and above not in h:
            o = above
            above = next_f(above)
        new_so.add(o)
    return list(new_so)


xs = [x.strip("\n") for x in open("input.txt", "r").readlines()]
X_DIM = len(xs[0])
Y_DIM = len(xs)

Os = set()
Hs = set()

for y in range(len(xs)):
    for x in range(len(xs[y])):
        v = xs[y][x]
        if v == "O":
            Os.add((x, y))
        elif v == "#":
            Hs.add((x, y))

# north
Os = advance(
    Os, Hs, lambda x: x[1] < 0, lambda x: (x[0], x[1] - 1), lambda x: x[1], False
)
load = 0
for o in Os:
    load += Y_DIM - o[1]

print(load)

# part two
Os = []
Hs = set()

for y in range(len(xs)):
    for x in range(len(xs[y])):
        v = xs[y][x]
        if v == "O":
            Os.append((x, y))
        elif v == "#":
            Hs.add((x, y))

from collections import defaultdict

seen = defaultdict(list)

i = 0
while True:
    period = None
    # north
    Os = advance(
        Os, Hs, lambda x: x[1] < 0, lambda x: (x[0], x[1] - 1), lambda x: x[1], False
    )

    # west
    Os = advance(
        Os, Hs, lambda x: x[0] < 0, lambda x: (x[0] - 1, x[1]), lambda x: x[0], False
    )

    # south
    Os = advance(
        Os,
        Hs,
        lambda x: x[1] > Y_DIM - 1,
        lambda x: (x[0], x[1] + 1),
        lambda x: x[1],
        True,
    )

    # east
    Os = advance(
        Os,
        Hs,
        lambda x: x[0] > X_DIM - 1,
        lambda x: (x[0] + 1, x[1]),
        lambda x: x[0],
        True,
    )

    k = tuple(sorted(Os))
    seen[k].append(i)

    if len(seen[k]) > 1:
        period = seen[k][1] - seen[k][0]

    if period and i % period == (1000000000 - 1) % period:
        load = 0
        for o in Os:
            load += Y_DIM - o[1]
        print(load)
        break
    i += 1
