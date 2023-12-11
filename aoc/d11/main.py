xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
G = {}
GALAXIES = []

expanded_lines = []

transposed_lines = list(zip(*xs))
transposed_lines = [''.join(t) for t in transposed_lines]
for t in transposed_lines:
    expanded_lines.append(t)
    if "#" not in t:
        expanded_lines.append(t)

transposed_lines = expanded_lines
expanded_lines = []
transposed_lines = list(zip(*transposed_lines))
transposed_lines = [''.join(t) for t in transposed_lines]
for t in transposed_lines:
    expanded_lines.append(t)
    if "#" not in t:
        expanded_lines.append(t)

xs = expanded_lines

for y in range(len(xs)):
    for x in range(len(xs[y])):
        c = xs[y][x]
        G[(x,y)] = c
        if c == '#':
            GALAXIES.append((x,y))

from itertools import combinations

lengths_sum = 0
for c in combinations(GALAXIES, 2):
    md = abs(c[0][0]-c[1][0]) + abs(c[0][1]-c[1][1])
    lengths_sum += md

print(lengths_sum)

# part two

FACTOR = 1000000

xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
G = {}
GALAXIES = []
EXPANDED_COLUMNS = []
EXPANDED_ROWS  = []

for i, v in enumerate(xs):
    if '#' not in v:
        EXPANDED_ROWS.append(i)

transposed_lines = list(zip(*xs))
transposed_lines = [''.join(t) for t in transposed_lines]
for i, v in enumerate(transposed_lines):
    if '#' not in v:
        EXPANDED_COLUMNS.append(i)

for y in range(len(xs)):
    for x in range(len(xs[y])):
        c = xs[y][x]
        G[(x,y)] = c
        if c == '#':
            GALAXIES.append((x,y))

lengths_sum2 = 0
for c in combinations(GALAXIES, 2):
    g1 = c[0]
    g2 = c[1]
    dist = 0
    x_start = min(g1[0], g2[0])
    x_end = max(g2[0], g1[0])
    y_start = min(g1[1], g2[1])
    y_end = max(g2[1], g1[1])
    
    while x_start < x_end:
        if x_start in EXPANDED_COLUMNS:
            dist += FACTOR
        else:
            dist += 1
        x_start += 1
    while y_start < y_end:
        if y_start in EXPANDED_ROWS:
            dist += FACTOR
        else:
            dist += 1
        y_start += 1
    lengths_sum2 += dist

print(lengths_sum2)