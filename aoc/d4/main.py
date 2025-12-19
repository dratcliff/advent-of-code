xs = [x.strip() for x in open('p1.txt').readlines()]
H = len(xs)
W = len(xs[0])
G = {}
for i in range(H):
    for j in range(W):
        G[(j, i)] = xs[i][j]

OFFSETS = [
    (0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)
]

total = 0
for y in range(H):
    for x in range(W):
        cur = (x,y)
        cur_char = G[(x,y)]
        if cur_char != '@':
            continue
        adj = 0
        for o in OFFSETS:
            nxt = (x+o[0],y+o[1])
            if nxt in G and G[nxt] == '@':
                adj += 1
        if adj < 4:
            total += 1
print("p1:", total)

total = 0
was_removed = True
while was_removed:
    was_removed = False
    nxt_G = {}
    for y in range(H):
        for x in range(W):
            cur = (x,y)
            cur_char = G[(x,y)]
            if cur_char != '@':
                nxt_G[cur] = cur_char
                continue
            adj = 0
            for o in OFFSETS:
                nxt = (x+o[0],y+o[1])
                if nxt in G and G[nxt] == '@':
                    adj += 1
            if adj < 4:
                total += 1
                nxt_G[cur] = '.'
                was_removed = True
            else:
                nxt_G[cur] = '@'
    G = nxt_G

print("p2:", total)
