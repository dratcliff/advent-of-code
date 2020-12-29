from itertools import permutations

def parse(filename):
    entries = [line.strip('\n') for line in open(filename)]
    entries = [x.split(' ') for x in entries]
    entries = [(x[0], x[2], int(x[3]), x[10][:-1]) for x in entries]

    for i in range(0, len(entries)):
        e = entries[i]
        if e[1] == "lose":
            entries[i] = (e[0], e[2]*-1, e[3])
        else:
            entries[i] = (e[0], e[2], e[3])
    return entries

def get_happiness_map(entries):
    m = {}
    for e in entries:
        if e[0] not in m:
            m[e[0]] = {}
        m[e[0]][e[2]] = e[1]
    return m

def max_happiness(m):
    hs = set()
    for p in permutations(m.keys(), len(m.keys())):
        p = list(p)
        h = 0

        h += m[p[0]][p[-1]]
        h += m[p[-1]][p[0]]

        for i in range(0, len(p) - 1):
            h += m[p[i]][p[i+1]]
            h += m[p[i+1]][p[i]]
        hs.add(h)
    return max(hs)

def test_day_thirteen():
    entries = parse("Day13sample.txt")
    m = get_happiness_map(entries)
    h = max_happiness(m)
    assert 330 == h

def day_thirteen():
    entries = parse("Day13.txt")
    m = get_happiness_map(entries)
    h = max_happiness(m)
    print(h)

def day_thirteen_p2():
    entries = parse("Day13.txt")
    m = get_happiness_map(entries)
    m["me"] = {}
    for k in m:
        m["me"][k] = 0
        m[k]["me"] = 0
    h = max_happiness(m)
    print(h)

if __name__=="__main__":
    test_day_thirteen()
    day_thirteen()
    day_thirteen_p2()