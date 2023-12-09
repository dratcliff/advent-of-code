xs = [x.strip('\n').split() for x in open('input.txt', 'r')]
xs = [list(map(int, x)) for x in xs]

extrapolated_values = []

for x in xs:
    diffs = []
    next_diffs = [x[i+1] - x[i] for i in range(len(x)-1)]
    diffs.append(next_diffs)
    while len(set(next_diffs)) != 1:
        next_diffs = [next_diffs[i+1] - next_diffs[i] for i in range(len(next_diffs)-1)]
        diffs.append(next_diffs)

    for i in range(len(diffs)-1,0,-1):
        diffs[i-1].append(diffs[i-1][-1]+diffs[i][-1])
    
    ev = x[-1]+diffs[0][-1]
    # x.append(ev)
    extrapolated_values.append(ev)

print(sum(extrapolated_values))

# part two

extrapolated_values = []

for x in xs:
    diffs = []
    next_diffs = [x[i+1] - x[i] for i in range(len(x)-1)]
    diffs.append(next_diffs)
    while len(set(next_diffs)) != 1:
        next_diffs = [next_diffs[i+1] - next_diffs[i] for i in range(len(next_diffs)-1)]
        diffs.append(next_diffs)

    for i in range(len(diffs)-1,0,-1):
        diffs[i-1] = [diffs[i-1][0]-diffs[i][0]] + diffs[i-1]
    
    ev = x[0]-diffs[0][0]
    extrapolated_values.append(ev)

print(sum(extrapolated_values))