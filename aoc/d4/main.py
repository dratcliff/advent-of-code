xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
xs = [x.split(": ")[1] for x in xs]
xs = [x.split(" | ") for x in xs]
xs = [(set(x[0].split()), set(x[1].split())) for x in xs]

s = 0
for x in xs:
    win_ct = len(x[0] & x[1])
    card_value = 0
    if win_ct == 1:
        card_value = 1
    elif win_ct > 1:
        card_value = 2**(win_ct-1)
    s += card_value

print(s)

## part two

card_ct = {}

for i in range(0, len(xs)):
    card_ct[i] = 1

for i in range(0, len(xs)):
    x = xs[i]
    win_ct = len(x[0]&x[1])
    if win_ct > 0:
        for j in range(1, win_ct+1):
            card_ct[i+j] += card_ct[i]
    
print(sum(card_ct.values()))

