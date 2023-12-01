def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()


def dist(s, b):
    return abs(s[0]-b[0]) + abs(s[1]-b[1])


def mark(row):
    intervals = []
    for s in sensors:
        sx, sy, sdist = s[0][0], s[0][1], s[2]
        if abs(row - sy) >= s[2]:
            continue
        minx = sx-abs(sdist-abs(row-sy))
        maxx = sx+abs(sdist-abs(row-sy))
        intervals.append([minx, maxx])
    intervals = sorted(intervals)
    return intervals


lines = get_data('input.txt')
lines = lines.strip().split('\n')
lines = [x.replace("Sensor at ", "").replace(
    " closest beacon is at ", "").split(":") for x in lines]

sensors = []

for line in lines:
    s = line[0].split(", ")
    sx = int(s[0][2:])
    sy = int(s[1][2:])
    s = (sx, sy)
    b = line[1].split(", ")
    bx = int(b[0][2:])
    by = int(b[1][2:])
    b = (bx, by)
    sensors.append((s, b, dist(s, b)))


def collapse(intervals: list):
    ret = []
    if len(intervals) <= 1:
        return intervals
    cur = intervals.pop(0)
    while intervals:
        n = intervals.pop(0)
        if cur[1] >= n[0]:
            cur = [cur[0], max(cur[1], n[1])]
        else:
            ret.append([cur[0], cur[1]])
            cur = n
    ret.append(cur)
    return ret


part_one_interval = collapse(mark(2000000))
print(abs(part_one_interval[0][1]-part_one_interval[0][0]))

avg_sensor_y = sum([x[0][1] for x in sensors])//len(sensors)

i = 1
found = False
while not found:
    for j in (i, -i):
        row = avg_sensor_y + j
        collapsed = collapse(mark(row))
        if len(collapsed) == 2:
            found = True
            gap = collapsed[0][1]+1
            freq = gap*4000000 + row
            print(freq)
            break
    i += 1
