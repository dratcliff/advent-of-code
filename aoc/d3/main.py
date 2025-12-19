xs = [x.strip() for x in  open('p1.txt').readlines()]
total = 0
for x in xs:
    max_joltage = 0
    for i in range(len(x)-1):
        for j in range(i+1, len(x)):
            joltage = int(x[i]+x[j])
            if joltage > max_joltage:
                max_joltage = joltage
    total += max_joltage

print("p1:", total)

from collections import deque

def check(my_string):
    Q = deque()
    seen = set()
    max_joltage = 0
    max_joltage_str = "0"*12
    for i in range(len(my_string)):
        Q.append((i, [my_string[i]]))
    while Q:
        pos, cur = Q.pop()
        key = (pos,) + tuple(cur)
        if key in seen:
            continue
        seen.add(key)
        joltage_str = ''.join(cur)
        joltage = int(joltage_str)
        comp_max_joltage = int(max_joltage_str[:len(joltage_str)])
        if joltage < comp_max_joltage:
            continue
        if len(cur) == 12:
            if joltage > max_joltage:
                max_joltage = joltage
                max_joltage_str = joltage_str
            continue
        for i in range(pos+1, len(my_string)):
            Q.append((i, cur + [my_string[i]]))
    return max_joltage

joltage_total = 0
for x in xs:
    joltage_total += check(x)

print("p2:", joltage_total)