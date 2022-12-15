import collections
from itertools import combinations
from collections import defaultdict
from itertools import combinations, permutations
from utilaoc import line_separated_file_to_2d

actual = line_separated_file_to_2d("b.txt")
actual = [x[1:] for x in actual]
actual = [[[int(x) for x in y.split(",")] for y in z] for z in actual]

counts = defaultdict(set)

def check(scanner, scanner1):
    for p in permutations((0, 1, 2)):
        scanner2 = []
        for s in scanner1:
            scanner2.append([s[p[i]] for i in range(0, 3)])
        counts = defaultdict(set)
        for c in combinations(scanner, 2):
            for d in combinations(scanner2, 2):
                c0 = (abs(c[0][0]-c[1][0]),
                      abs(c[0][1]-c[1][1]), abs(c[0][2]-c[1][2]))
                d0 = (abs(d[0][0]-d[1][0]),
                      abs(d[0][1]-d[1][1]), abs(d[0][2]-d[1][2]))
                # print(c, d, c0, d0)
                if c0 == d0:
                    counts[(tuple(c[0]), tuple(d[0]))].add(
                        (tuple(c[1]), tuple(d[1])))
                    if len(counts[(tuple(c[0]), tuple(d[0]))]) >= 11:
                        return counts[(tuple(c[0]), tuple(d[0]))], p
                    counts[(tuple(c[1]), tuple(d[0]))].add(
                        (tuple(c[0]), tuple(d[1])))
                    if len(counts[(tuple(c[1]), tuple(d[0]))]) >= 11:
                        return counts[(tuple(c[1]), tuple(d[0]))], p
                    counts[(tuple(c[0]), tuple(d[1]))].add(
                        (tuple(c[1]), tuple(d[0])))
                    if len(counts[(tuple(c[0]), tuple(d[1]))]) >= 11:
                        return counts[(tuple(c[0]), tuple(d[1]))], p
                    counts[(tuple(c[1]), tuple(d[1]))].add(
                        (tuple(c[0]), tuple(d[0])))
                    if len(counts[(tuple(c[1]), tuple(d[1]))]) >= 11:
                        return counts[(tuple(c[1]), tuple(d[1]))], p

    return None


def sign(a):
    if a > 0:
        return 1
    elif a == 0:
        return 0
    else:
        return -1


offsets = {}
scanners = set()


def calc_offset(path, k):
    global offsets

    i = path[k]
    j = path[k+1]

    if (i, j) not in overlap:
        raise Exception("wat")
    o = overlap[(i, j)]
    o_pairs = list(o[0])
    o_perm = o[1]
    first_pair = o_pairs[0]
    second_pair = o_pairs[1]

    xm = 1
    ym = 1
    zm = 1

    if sign(first_pair[0][0] - second_pair[0][0]) != \
            sign(first_pair[1][0] - second_pair[1][0]):
        xm = -1
    if sign(first_pair[0][1] - second_pair[0][1]) != \
            sign(first_pair[1][1] - second_pair[1][1]):
        ym = -1
    if sign(first_pair[0][2] - second_pair[0][2]) != \
            sign(first_pair[1][2] - second_pair[1][2]):
        zm = -1

    ox = first_pair[0][0] - xm*first_pair[1][0]
    oy = first_pair[0][1] - ym*first_pair[1][1]
    oz = first_pair[0][2] - zm*first_pair[1][2]
    scanners.add((ox, oy, oz))
    if k == 0:
        if (i, j) not in offsets:
            offsets[(i, j)] = (ox, oy, oz, xm, ym, zm)
    else:
        prev = offsets[(path[k-1], path[k])]
        offsets[(i, j)] = (ox+prev[0], oy+prev[1], oz+prev[2])


to_do = collections.deque()
overlap = defaultdict(tuple)
to_do.append(0)
done = set()
adjusted = set()
adjusted.add(0)
while to_do:
    i = to_do.pop()
    for j in range(0, len(actual)):
        if i != j and (i, j) not in done and (j, i) not in done:
            scanner = actual[i]
            scanner1 = actual[j]
            r = check(scanner, scanner1)
            done.add((i,j))
            if r != None:
                done.add((i, j))
                to_do.append(j)
                overlap[(i, j)] = r
                perm = r[1]
                calc_offset([i, j], 0)
                if j not in adjusted:
                    adjusted.add(j)
                    adjusted_actual = []
                    offset = offsets[(i, j)]
                    for k in actual[j]:
                        adjusted_actual.append([k[perm[0]]*offset[3]+offset[0],
                                                k[perm[1]]*offset[4]+offset[1], k[perm[2]]*offset[5]+offset[2]])
                    actual[j] = adjusted_actual


all_beacons = set()
for i in range(0, len(actual)):
    if i not in adjusted:
        raise Exception("omg")
    for k in actual[i]:
        all_beacons.add(tuple(k))

print(len(all_beacons))

md = 0
for c in combinations(scanners, 2):
    this_md = abs(c[0][0]-c[1][0]) + abs(c[0][1] -
                                         c[1][1]) + abs(c[0][2]-c[1][2])
    if this_md > md:
        md = this_md

print(md)
