xs = [x.split('\n') for x in open('input.txt', 'r').read().split('\n\n')]

def triangle(rows):
    res = []
    for i in range(rows-1):
        res2 = []
        res2.append((i,i+1))
        j = i-1
        k = i+2
        while j >=0 and k <= rows-1:
            res2.append((j,k))
            j-=1
            k+=1

        res.append(res2)
    return res

def horizontal(p):
    return vertical([''.join(x) for x in list(zip(*p))])

def vertical(p):
    res = ()
    for t in triangle(len(p[0])):
        found = True
        for row in p:
            for e in t:
                if row[e[0]] != row[e[1]]:
                    found = False
                    break
        if found:
            res.append(min(t, key=lambda x: abs(x[0]-x[1])))
    return res

ct = 0
for x in xs:
    v = vertical(x)
    if v:
        ct += v[0][0]+1
    else:
        ct += (horizontal(x)[0][0]+1)*100
print(ct)

# part two
ct = 0
for e in xs:
    _v = vertical(e)
    _v = _v[0] if _v else None
    _h = horizontal(e)
    _h = _h[0] if _h else None
    found = False
    for y in range(len(e)):
        if not found:
            for x in range(len(e[y])):
                if not found:
                    old = e[y][x]
                    new = '.' if old == '#' else '#'
                    z = list(e[y])
                    z[x] = new
                    e[y] = ''.join(z)
                    v = vertical(e)
                    h = horizontal(e)
                    if len(v) > 1:
                        v = v[0] if v[1] == _v else v[1]
                    else:
                        v = None if len(v) == 0 else v[0]
                    if len(h) > 1:
                        h = h[0] if h[1] == _h else h[1]
                    else:
                        h = None if len(h) == 0 else h[0]
                    if v != _v and v:
                        ct += v[0]+1
                        found = True
                    elif h != _h and h:
                        found = True
                        ct += (h[0]+1)*100
                    z[x] = old
                    e[y] = ''.join(z)

print(ct)