from collections import Counter

card_values = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}

def my_sort(hand):
    c = Counter(hand[0])
    strength = 0
    counts = sorted(c.values(), reverse=True)
    match len(counts):
        case 1:
            strength = 6
        case 2:
            strength = counts[0]+1 # 5 or 4
        case 3:
            if counts[0] == 3:
                strength = 3
            if counts[1] == 2:
                strength =  2
        case 4:
            strength = 1
        case 5:
            strength = 0

    return [strength] + [card_values[x] for x in hand[0]]




xs = [x.strip('\n').split() for x in open('input.txt', 'r').readlines()]
xs = list(sorted(xs, key=my_sort))

winnings = 0
for i in range(len(xs)):
    x = xs[i]
    winnings += (i+1)*int(x[1])

print(winnings)

# part two

card_values['J'] = 1

def my_sort2(hand):
    c = Counter(hand[0])
    strength = 0
    counts = sorted(c.values(), reverse=True)
    js = sum([1 for x in hand[0] if x == 'J'])
    match len(counts):
        case 1:
            strength = 6
        case 2:
            strength = counts[0]+1 # 5 or 4
            # (4,1) or (3,2)
            if js > 0:
                strength = 6
        case 3:
            if counts[0] == 3:
                # (3,1,1) or (2,2,1)
                strength = 3
                if js > 0:
                    strength = 5
            else:
                strength =  2
                if js == 2:
                    strength = 5
                if js == 1:
                    strength = 4
        case 4:
            # (2,1,1,1)
            strength = 1
            if js > 0:
                strength = 3
        case 5:
            strength = 0
            if js > 0:
                strength = 1
    return [strength] + [card_values[x] for x in hand[0]]

xs = [x.strip('\n').split() for x in open('input.txt', 'r').readlines()]
xs = list(sorted(xs, key=my_sort2))

winnings = 0
for i in range(len(xs)):
    x = xs[i]
    winnings += (i+1)*int(x[1])

print(winnings)