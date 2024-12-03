from math import lcm
xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]

instructions = xs[0]
rest = xs[2:]

M = {}

rest = [x.split(" = ") for x in rest]
for r in rest:
    node = r[0]
    left = r[1][1:4]
    right = r[1][6:9]

    M[node] = {}
    M[node]['L'] = left
    M[node]['R'] = right


ct = 0
i = 0
instruction = None
cur = 'AAA'
while cur != 'ZZZ':
    instruction = instructions[i % len(instructions)]
    cur = M[cur][instruction]
    i += 1
    ct += 1

print(ct)

# part two

start_nodes = [x for x in M.keys() if x[-1] == 'A']
end_nodes = [x for x in M.keys() if x[-1] == 'Z']
counts = []
for sn in start_nodes:
    ct = 0
    i = 0
    instruction = None
    cur = sn
    while cur not in end_nodes:
        instruction = instructions[i % len(instructions)]
        cur = M[cur][instruction]
        i += 1
        ct += 1
    counts.append(ct)


print(lcm(*counts))
