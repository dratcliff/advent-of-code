from utilaoc import file_to_strings

# sample = file_to_strings("sample.txt")
actual = file_to_strings("input.txt")

# print(sample)
# print(actual)


l = 12

ones = [0] * l
zeroes = [0] * l

for a in actual:
    for i in range(0, len(a)):
        if a[i] == '1':
            ones[i] += 1
        elif a[i] == '0':
            zeroes[i] += 1

print(zeroes)
print(ones)

def oxy(all, pos, cur):
    one = 0
    zero = 0
    for a in all:
        if a[pos] == '1':
            one += 1
        else:
            zero += 1
    if one >= zero:
        cur[pos] = '1'
    else:
        cur[pos] = '0'

    n = []
    for a in all:
        if a[pos] == cur[pos]:
            n.append(a)
    return n

init_oxy = [0] * l

c = oxy(actual, 0, init_oxy)
for i in range(1, l):
    c = oxy(c, i, init_oxy)


def scrub(all, pos, cur):
    one = 0
    zero = 0
    for a in all:
        if a[pos] == '1':
            one += 1
        else:
            zero += 1
    if one < zero:
        cur[pos] = '1'
    else:
        cur[pos] = '0'

    n = []
    for a in all:
        if a[pos] == cur[pos]:
            n.append(a)
    
    return n

init_scrub = [0] * l
d = scrub(actual, 0, init_scrub)

for i in range(1, l):
    d = scrub(d, i, init_scrub)
    if len(d) == 1:
        break

print(c)
print(d)

print(int(c[0],2)*int(d[0],2))
