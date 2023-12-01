import re
from collections import deque


def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()

# This used to look nicer, but I never figured out a
# very efficient way to solve this, so I trashed everything
# trying to save memory. I think if I'd done this on
# my laptop with 64GB RAM I would've been done a long time ago,
# but the 16GB on my desktop seems like it's right around the limit
# of what my deque takes up.

# Ultimately, I think the garbage heuristic I added is probably enough
# to save this code from running indefinitely, but I'm
# not even really sure that it's guaranteed to work. :shrug:


lines = get_data('input.txt')
lines = lines.strip().split('\n')
lines = lines[:3]
s = 1

# 0=ore, 1=clay, 2=obsidian, 3=geode
# should've left the named tuple but I'm committed to it at this point
for line in lines:
    matches = re.findall(r'(\d+)', line)
    costs = {
        "id": int(matches[0]),
        0: {
            0: int(matches[1])
        },
        1: {
            0: int(matches[2])
        },
        2: {
            0: int(matches[3]),
            1: int(matches[4])
        },
        3: {
            0: int(matches[5]),
            2: int(matches[6])
        }
    }

    rc = (1, 0, 0, 0)
    oc = (0, 0, 0, 0)
    Q = deque()
    Q.append((rc, oc, 0, 0))
    Q.append((rc, oc, 0, 1))
    best = 0
    seen = set()
    earliest = [33]*5
    while Q:
        rc, oc, elapsed, next_robot = Q.pop()
        skip = False
        for i in range(0, 5):
            if rc[3] > i and elapsed < earliest[i]:
                earliest[i] = elapsed
            if elapsed > earliest[i] and rc[3] < i+1:
                skip = True
                break
        if skip:
            continue
        if (rc, oc, elapsed, next_robot) in seen:
            continue
        if oc[3] > best:
            best = oc[3]
        if elapsed >= 32:
            continue
        if next_robot == 0:
            if oc[0] >= costs[0][0]:
                next_oc = (oc[0]+rc[0]-costs[0][0], oc[1]+rc[1],
                           oc[2]+rc[2], oc[3]+rc[3])
                next_rc = (rc[0]+1, rc[1], rc[2], rc[3])
                Q.append((next_rc, next_oc, elapsed+1, 0))
                Q.append((next_rc, next_oc, elapsed+1, 1))
                Q.append((next_rc, next_oc, elapsed+1, 2))
                Q.append((next_rc, next_oc, elapsed+1, 3))
            else:
                next_oc = (oc[0]+rc[0], oc[1]+rc[1],
                           oc[2]+rc[2], oc[3]+rc[3])
                next_rc = (rc[0], rc[1], rc[2], rc[3])
                Q.append((next_rc, next_oc, elapsed+1, 0))
        elif next_robot == 1:
            if oc[0] >= costs[1][0]:
                next_oc = (oc[0]+rc[0]-costs[1][0], oc[1]+rc[1],
                           oc[2]+rc[2], oc[3]+rc[3])
                next_rc = (rc[0], rc[1]+1, rc[2], rc[3])
                Q.append((next_rc, next_oc, elapsed+1, 0))
                Q.append((next_rc, next_oc, elapsed+1, 1))
                Q.append((next_rc, next_oc, elapsed+1, 2))
                if rc[2] > 0:
                    Q.append((next_rc, next_oc, elapsed+1, 3))
            else:
                next_oc = (oc[0]+rc[0], oc[1]+rc[1],
                           oc[2]+rc[2], oc[3]+rc[3])
                next_rc = (rc[0], rc[1], rc[2], rc[3])
                Q.append((next_rc, next_oc, elapsed+1, 1))
        elif next_robot == 2:
            if oc[0] >= costs[2][0] and oc[1] >= costs[2][1]:
                next_oc = (oc[0]+rc[0]-costs[2][0], oc[1]+rc[1]-costs[2][1],
                           oc[2]+rc[2], oc[3]+rc[3])
                next_rc = (rc[0], rc[1], rc[2]+1, rc[3])
                if next_oc[0] >= costs[3][0] and next_oc[2] >= costs[3][2]:
                    Q.append((next_rc, next_oc, elapsed+1, 3))
                else:
                    Q.append((next_rc, next_oc, elapsed+1, 0))
                    Q.append((next_rc, next_oc, elapsed+1, 1))
                    Q.append((next_rc, next_oc, elapsed+1, 2))
                    Q.append((next_rc, next_oc, elapsed+1, 3))
            else:
                next_oc = (oc[0]+rc[0], oc[1]+rc[1],
                           oc[2]+rc[2], oc[3]+rc[3])
                next_rc = (rc[0], rc[1], rc[2], rc[3])
                Q.append((next_rc, next_oc, elapsed+1, 2))
        elif next_robot == 3:
            if oc[0] >= costs[3][0] and oc[2] >= costs[3][2]:
                next_oc = (oc[0]+rc[0]-costs[3][0], oc[1]+rc[1],
                           oc[2]+rc[2]-costs[3][2], oc[3]+rc[3])
                next_rc = (rc[0], rc[1], rc[2], rc[3]+1)
                if next_oc[0] >= costs[3][0] and next_oc[2] >= costs[3][2]:
                    Q.append((next_rc, next_oc, elapsed+1, 3))
                else:
                    Q.append((next_rc, next_oc, elapsed+1, 0))
                    Q.append((next_rc, next_oc, elapsed+1, 1))
                    Q.append((next_rc, next_oc, elapsed+1, 2))
                    Q.append((next_rc, next_oc, elapsed+1, 3))
            else:
                next_oc = (oc[0]+rc[0], oc[1]+rc[1],
                           oc[2]+rc[2], oc[3]+rc[3])
                next_rc = (rc[0], rc[1], rc[2], rc[3])
                Q.append((next_rc, next_oc, elapsed+1, 3))
        seen.add((rc, oc, elapsed, next_robot))
    print("output for id", costs["id"], "is", best)
    s *= best

print(s)
