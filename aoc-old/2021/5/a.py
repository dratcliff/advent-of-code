from utilaoc import file_to_strings

actual = file_to_strings("input.txt")
actual = [x.split(' -> ') for x in actual]

from collections import defaultdict

grid = defaultdict(int)

for a in actual:
    start = a[0]
    end = a[1]

    start = start.split(',')
    start = [int(x) for x in start]
    end = end.split(',')
    end = [int(x) for x in end]

    if start[0] == end[0]: # horizontal
        if end[1] < start[1]:
            temp = start
            start = end
            end = temp
        for i in range(start[1], end[1]+1):
            grid[(start[0], i)] += 1
    elif start[1] == end[1]: # vertical
        if end[0] < start[0]:
            temp = start
            start = end
            end = temp
        for i in range(start[0], end[0]+1):
            grid[(i, start[1])] += 1
    else: # diagonal -- comment out this else block for part 1
        if end[0] < start[0]:
            temp = start
            start = end
            end = temp
        inc = 1
        if end[1] < start[1]:
            inc = -1
        for i in range(0, end[0]-start[0]+1):
            grid[(start[0]+i, start[1] + i*inc)] += 1

s = 0
for k, v in grid.items():
    if v > 1:
        s += 1

print(s)