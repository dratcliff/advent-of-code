xs = [x.strip() for x in open('p1.txt').readlines()]
xs = [x.split(',') for x in xs]
xs = [y.split('-') for x in xs for y in x]
xs = [[int(y) for y in x] for x in xs] 

def has_repeat(i, num_repeats):
    i_str = str(i)
    j = len(i_str)
    if j%num_repeats != 0:
        return False
    j = int(j/num_repeats)
    segments = set()
    for s in range(0, len(i_str), j):
        segments.add(i_str[s:s+j])
        if len(segments) > 1:
            return False
    return True

p1 = 0
p2 = 0
for x in xs:
    for i in range(x[0], x[1]+1):
        i_str = str(i)
        max_size = len(i_str)//2
        for j in range(2, len(i_str)+1):
            if has_repeat(i, j):
                if j == 2:
                    p1 += i
                p2 += i
                break
print(p1)
print(p2)