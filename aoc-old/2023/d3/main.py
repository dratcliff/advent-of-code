from collections import defaultdict

xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]

nums = []
gear_adj = defaultdict(list)

for y in range(len(xs)):
    in_number = False
    retain = False
    gears = set()
    s = ""

    for x in range(len(xs[y])):
        c = xs[y][x]
        if c.isnumeric():
            if not in_number:
                in_number = True
            s += c
            for D in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                dy = y+D[1]
                dx = x+D[0]
                if 0 <= dx < len(xs[y]) and 0 <= dy < len(xs):
                    dc = xs[dy][dx]
                    if not dc.isnumeric() and dc != ".":
                        retain = True
                    if dc == "*":
                        gears.add((dx, dy))
        if not c.isnumeric() or x == len(xs[y])-1:
            if in_number and retain:
                nums.append(s)
                if len(gears) > 0:
                    for gear in gears:
                        gear_adj[gear].append(int(s))
            in_number = False
            retain = False
            s = ""
            gears = set()


nums = [int(x) for x in nums]
print(sum(nums))

ratios = 0
for k, v in gear_adj.items():
    if len(v) == 2:
        gear_list = v
        ratios += gear_list[0]*gear_list[1]

print(ratios)
