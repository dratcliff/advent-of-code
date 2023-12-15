xs = open('input.txt', 'r').read().replace('\n', '').split(",")

def hash(e):
    h = 0
    for x in e:
        asc = ord(x)
        h += asc
        h *= 17
        h %= 256
    return h

res = 0
for e in xs:
    res += hash(e)

print(res)

# part two
from collections import defaultdict
M = defaultdict(list)
for e in xs:
    if "=" not in e:
        label = e[:-1]
        label_hash = hash(label)
        box = M[label_hash]
        idx = -1
        for i, v in enumerate(box):
            if v[0] == label:
                idx = i
                break
        if idx != -1:
            M[label_hash] = box[:idx] + box[idx+1:]

    else:
        label = e.split("=")[0]
        label_hash = hash(label)
        val = int(e.split("=")[1])
        idx = -1
        box = M[label_hash]
        for i, v in enumerate(box):
            if v[0] == label:
                idx = i
                break
        if idx != -1:
            M[label_hash][idx] = (label, val)
        else:
            M[label_hash].append((label, val))

fp = 0
for bi, b in M.items():
    for i, v in enumerate(b):
        fp += ((bi+1)*(i+1)*v[1])

print(fp)