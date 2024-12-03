from collections import deque
import math

xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
xs = [x.split(' -> ') for x in xs]

flips = {}
cons = {}
outs = set()

broadcaster = []

for x in xs:
    src, dest = x
    dests = dest.split(', ')
    if src[0] == '%':
        src = src[1:]
        assert src not in cons
        flips[src] = {}
        flips[src]['dests'] = dests
        flips[src]['toggle'] = False
    elif src[0] == '&':
        src = src[1:]
        assert src not in flips
        cons[src] = {}
        cons[src]['dests'] = dests
        cons[src]['inputs'] = {}
    elif src == 'broadcaster':
        broadcaster.extend(dests)

for f, v in flips.items():
    for dest in v['dests']:
        if dest in cons:
            cons[dest]['inputs'][f] = False
        elif dest in flips:
            pass
        else:
            outs.add(dest)

for f, v in cons.items():
    for dest in v['dests']:
        if dest in cons:
            cons[dest]['inputs'][f] = False
        elif dest in flips:
            pass
        else:
            outs.add(dest)


high = 0
low = 0
times = 100000000
found = set()
for i in range(times):
    if len(found) == 4:
        break
    low += 1
    Q = deque()

    for b in broadcaster:
        Q.append((b, False, 'broadcaster'))

    while Q:
        dest, pulse, src = Q.popleft()
        if pulse == True:
            high += 1
        else:
            low += 1
        if dest in cons:
            if dest == 'dt' and pulse != cons[dest]['inputs'][src]:
                found.add(i+1)
                if len(found) == 4:
                    print(math.lcm(*found))
                    break
            con = cons[dest]
            con['inputs'][src] = pulse
            all_high = True
            for k, v in con['inputs'].items():
                if v == False:
                    all_high = False
                    break
            pulse = True
            if all_high:
                pulse = False
            for d in con['dests']:
                Q.append((d, pulse, dest))
        elif dest in flips:
            if pulse == True:
                pass
            else:
                flip = flips[dest]
                pulse = False
                if flip['toggle'] == False:
                    flip['toggle'] = True
                    pulse = True
                else:
                    flip['toggle'] = False
                    pulse = False
                for d in flip['dests']:
                    Q.append((d, pulse, dest))
        elif dest in outs:
            pass
        else:
            raise Exception("what", dest, pulse, src)

    if i+1 == 1000:
        print(high, low, high*low)
