xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
xs = [[y for y in x if str.isnumeric(y)] for x in xs]
xs = [(int(x[0]), int(x[-1])) for x in xs]
xs = [x[0]*10+x[1] for x in xs]
print(sum(xs))

# part two
xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]

replacements = {
    'one': 'o1e',
    'two': 't2o',
    'three': 't3e',
    'four': 'f4r',
    'five': 'f5e',
    'six': 's6x',
    'seven': 's7n',
    'eight': 'e8t',
    'nine': 'n9e'
}

xn = []
for line in xs:
    n = line
    for k, v in replacements.items():
        n = n.replace(k, v)
    xn.append(n)

xs = xn

xs = [[y for y in x if str.isnumeric(y)] for x in xs]
xs = [(int(x[0]), int(x[-1])) for x in xs]
xs = [x[0]*10+x[1] for x in xs]
print(sum(xs))