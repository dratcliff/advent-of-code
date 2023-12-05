xs = open('input.txt', 'r').read()
xs = xs.split('\n\n')
xs = [x.split('\n') for x in xs]

seeds = tuple(map(int, xs[0][0].replace("seeds: ", "").split()))

maps = {}
ranges = {}

for x in xs[1:]:
    k = None
    for e in x:
        if "-to-" in e:
            e = e.replace(" map:", "")
            e = e.split("-to-")
            k = e[0]
            maps[k] = e[1]
            ranges[k] = []
        elif len(e) > 0:
            ranges[k].append(tuple(map(int, e.split())))


def get_dest(src_type, src_no):
    global maps
    global ranges
    for dest, src, size in ranges[src_type]:
        if src+size >= src_no >= src:
            return (dest-src)+src_no
    return src_no


def get_seed_dest(seed_no):
    cur_type = 'seed'
    dest = get_dest('seed', seed_no)
    while cur_type in maps:
        cur_type = maps[cur_type]
        if cur_type != 'location':
            dest = get_dest(cur_type, dest)
    return dest


lowest_location = None

for seed in seeds:
    dest = get_seed_dest(seed)
    if not lowest_location or lowest_location > dest:
        lowest_location = dest

print(lowest_location)
print()

# part two

seed_intervals = []
for i in range(0, len(seeds)-1, 2):
    seed_intervals.append((seeds[i], seeds[i]+seeds[i+1]))


def get_next_interval(src_interval, src_type):
    global ranges
    intervals = sorted([(src, src+size-1, dest-src)
                       for (dest, src, size) in ranges[src_type]])
    _intervals = []

    # build a list of (start, end, offset)
    # filling in "gaps" with offset 0 when
    # source interval overlaps with mapped interval
    for i in range(len(intervals)):
        i_start, i_end, i_offset = intervals[i]
        _intervals.append((i_start, i_end, i_offset))
        if i == 0 and i_start > src_interval[0]:
            _intervals.append((src_interval[0], i_start-1, 0))
        elif i == len(intervals)-1:
            if src_interval[1] > i_end:
                _intervals.append((i_end+1, src_interval[1], 0))
        else:
            ni_start, ni_end, ni_offset = intervals[i+1]
            if ni_start - i_end > 1:
                _intervals.append((i_end+1, ni_start-1, 0))

    intervals = sorted(_intervals)

    # build a list of (start, end) by applying the offsets
    res = []
    for i_start, i_end, i_offset in intervals:
        if src_interval[0] > i_end or src_interval[1] < i_start:
            continue
        overlap_start = max(i_start, src_interval[0])
        overlap_end = min(i_end, src_interval[1])
        overlap = (overlap_start+i_offset, overlap_end+i_offset)
        # not necessary but makes things neater
        if overlap[0] != overlap[1]:
            res.append(overlap)

    return res


next_intervals = []
cur_type = 'seed'
while cur_type != 'location':
    for seed_interval in seed_intervals:
        _next_intervals = get_next_interval(seed_interval, cur_type)
        for _ni in _next_intervals:
            next_intervals.append(_ni)
    cur_type = maps[cur_type]
    seed_intervals = next_intervals
    next_intervals = []

print(min(seed_intervals, key=lambda x: x[0])[0])
