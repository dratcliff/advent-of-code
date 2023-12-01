import re
from collections import deque
from itertools import combinations


def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()


lines = get_data('input.txt')
valves = []
lines = lines.strip().split('\n')

for line in lines:
    m = re.findall(r'([A-Z][A-Z])', line)
    src = m[0]
    dests = m[1:]
    m = re.search(r'(\d+)', line)
    rate = int(m.group())
    valves.append((src, dests, rate))

rates = {}
neighbors = {}

for valve in valves:
    src, dest, rate = valve[0], valve[1], valve[2]
    rates[src] = rate
    neighbors[src] = dest

productive_valves = {k: v for k, v in rates.items() if v != 0}


sps = {}


def shortest_path(src, dest):
    if (src, dest) in sps:
        return sps[(src, dest)]
    i = 0
    seen = set()
    Q = deque()
    Q.append((src, ()))
    while Q:
        i += 1
        cur, path = Q.popleft()
        if cur == dest:
            sps[(src, dest)] = path + (dest,)
            return path + (dest,)
        if cur not in seen:
            for v in neighbors[cur]:
                Q.append((v, path + (cur,)))
        seen.add(cur)


def score(p, minutes):
    s = 0
    for k, v in enumerate(p):
        if v[-1] == "+":
            s += (minutes-(k))*rates[v[:-1]]
    return s


def most_pressure(valve_idxs, minutes):
    Q = deque()
    Q.append(('AA', ('AA',)))
    m = 0
    while Q:
        cur, path = Q.pop()
        for k in valve_idxs:
            if k != cur and k + "+" not in path:
                p = shortest_path(cur, k)
                new_path = path + p[1:] + (p[-1] + "+",)
                new_cur = p[-1]
                if len(new_path) < minutes:
                    Q.append((new_cur, new_path))
                else:
                    sc = score(new_path[:minutes], minutes)
                    if sc > m:
                        m = sc
            else:
                sc = score(path, minutes)
                if sc > m:
                    m = sc
    return m


print(most_pressure(productive_valves.keys(), 30))

key_idx = {k: v for k, v in enumerate(productive_valves.keys())}
mm = 0
for i in range((len(productive_valves)//2), (len(productive_valves)//2)+1):
    for c in combinations(key_idx.keys(), i):
        elephants = [v for k, v in key_idx.items() if k in c]
        mine = [v for k, v in key_idx.items() if v not in elephants]
        elephant_score = most_pressure(elephants, 26)
        my_score = most_pressure(mine, 26)
        s = elephant_score + my_score
        if s > mm:
            mm = s
            print(s, mine, elephants)
