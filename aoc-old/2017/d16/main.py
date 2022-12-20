def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()

lines = get_data('input.txt')
lines = lines.strip().split('\n')[0]
lines = lines.split(",")
lines = [((x[0],) + tuple(x[1:].split("/"))) for x in lines]
lines = [(x[0], int(x[1]), int(x[2])) if x[0] == 'x' else x for x in lines ]
lines = [(x[0], int(x[1])) if x[0] == "s" else x for x in lines]

programs = [chr(x) for x in range(ord('a'), ord('p')+1)]

from collections import deque
seen = {}
for i in range(0, 100):
    for line in lines:
        if line[0] == "s":
            D = deque(programs)
            D.rotate(line[1])
            programs = list(D)
        elif line[0] == "x":
            programs[line[1]], programs[line[2]] = programs[line[2]], programs[line[1]]
        elif line[0] == "p":
            t = programs.index(line[1])
            u = programs.index(line[2])
            programs[t], programs[u] = programs[u], programs[t]

    k = ''.join(programs)
    print(i, k)
    if k in seen.values():
        print("!",i)
        break
    seen[i] = k

print(seen[(1000000000-1) % 44])
