xs = open('input.txt', 'r').read().split('\n\n')
xs = [x.split('\n') for x in xs]
xs = [[x for x in y if len(x) > 0] for y in xs]

wf = xs[0]
ratings = xs[1]
ratings = [x[1:-1] for x in ratings]
ratings = [x.split(',') for x in ratings]
ratings = [[y.split('=') for y in x] for x in ratings]
ratings = [{x[0]: int(x[1]) for x in y} for y in ratings]


wf = [x.split('{') for x in wf]
wf = {x[0]: x[1].replace('}', "").split(',') for x in wf}

def get_wf(x, rating):
    for e in x:
        e = e.split(':')
        if len(e) == 1:
            return e[0]
        
        op_idx = e[0].find('<')
        if op_idx != -1:
            e = ('<', e[0][:op_idx], e[0][op_idx+1:], e[1])
        else:
            op_idx = e[0].find('>')
            assert op_idx != -1
            e = ('>', e[0][:op_idx], e[0][op_idx+1:], e[1])
        
        op, part, thresh, dest = e
        part_val = rating[part]
        thresh = int(thresh)
        if op == '<':
            if part_val < thresh:
                return dest
        elif op == '>':
            if part_val > thresh:
                return dest
        else:
            raise Exception

s = 0
for rating in ratings:
    cur = 'in'
    while cur not in ('A', 'R'):
        cur = get_wf(wf[cur], rating)
    if cur == 'A':
        s += sum(rating.values())

print(s)

# part two

def get_wf2(wf, rating):
    d = rating['dest']
    if d in ('A', 'R'):
        return rating
    x = wf[d]
    res = []
    for e in x:
        e = e.split(':')
        if len(e) == 1:
            r = {k: v for k, v in rating.items()}
            r['dest'] = e[0]
            res.append(r)
            continue
        op_idx = e[0].find('<')
        if op_idx != -1:
            e = ('<', e[0][:op_idx], e[0][op_idx+1:], e[1])
        else:
            op_idx = e[0].find('>')
            assert op_idx != -1
            e = ('>', e[0][:op_idx], e[0][op_idx+1:], e[1])
        op, part, thresh, dest = e
        thresh = int(thresh)
        if op == '<':
            r = {k: v for k, v in rating.items()}
            r['dest'] = dest
            new_part = (r[part][0],thresh-1)
            rating[part] = (thresh, r[part][1])
            r[part] = new_part
            res.append(r)
            continue
        elif op == '>':
            r = {k: v for k, v in rating.items()}
            r['dest'] = dest
            new_part = (thresh+1, r[part][1])
            rating[part] = (r[part][0], thresh)
            r[part] = new_part
            res.append(r)
            continue
        else:
            raise Exception
    return res

in_rating = {
    'x': (1, 4000),
    'm': (1, 4000),
    'a': (1, 4000),
    's': (1, 4000),
    'dest': 'in'
}
rs = get_wf2(wf, in_rating)
done = False
while not done:
    nrs = []
    done = True
    for r in rs:
        if r['dest'] not in ('A', 'R'):
            done = False
            nrs.extend(get_wf2(wf, r))
        else:
            nrs.append(r)
    rs = nrs

s = 0

for r in rs:
    if r['dest'] == 'A':
        p = 1
        p *= (r['x'][1]-r['x'][0]+1)
        p *= (r['m'][1]-r['m'][0]+1)
        p *= (r['a'][1]-r['a'][0]+1)
        p *= (r['s'][1]-r['s'][0]+1)
        s += p
print(s)