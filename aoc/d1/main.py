xs = open('p1.txt').readlines()
xs = [x.strip() for x in xs]

p1 = 0
p2 = 0
pos = 50
for x in xs:
    d = x[0]
    if d == 'L':
        d = -1
    else:
        d = 1
    m = int(x[1:])

    for i in range(m):
        pos += d
        pos %= 100
        if pos == 0:
            p2 += 1

    if pos == 0:
        p1 += 1
    
print(f"p1: {p1}\np2: {p2}")