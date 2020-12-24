import utils
from collections import defaultdict
from itertools import permutations

# crucial: https://math.stackexchange.com/questions/2254655/hexagon-grid-coordinate-system

my_perms = set()
for p in permutations([1, 1, 1, 0, 0, 0, -1, -1, -1], 3):
    my_perms.add(p)
my_perms.remove((0, 0, 0))
my_perms = set([x for x in my_perms if 0 in x])
my_perms = set([x for x in my_perms if sum(x) == 0])

def flip(line):
    x = 0 #se/nw
    y = 0 #sw/ne
    z = 0 #e/w
    for i in range(0, len(line)):
        cur = line[i]
        if cur == "se":
            z += 1
            y -= 1
        elif cur == "nw":
            y += 1
            z -= 1
        elif cur == "sw":
            x -= 1
            z += 1
        elif cur == "ne":
            x += 1
            z -= 1
        elif cur == "e":
            x += 1
            y -= 1
        elif cur == "w":
            x -= 1
            y += 1
        else:
            print("!!!")
    return (x, y, z)



def run(entries):

    lines = []
    for e in entries:
        line = []
        i = 0
        while i < len(e):
            if e[i] == "s" or e[i] == "n":
                line.append(e[i:i+2])
                i += 2
            else:
                line.append(e[i])
                i += 1
        if line[-1] == ",":
            line = line[:-1]
        lines.append(line)
    
    tiles = set()
    for line in lines:
        flipped = flip(line)
        if flipped in tiles:
            tiles.remove(flipped)
        else:
            tiles.add(flipped)
        
    for i in range(0, 100):
        next_black = set()
        white_adj_cts = defaultdict(set)
        next_white = set()
        for t in tiles:
            black_ct = 0
            for p in my_perms:
                if (t[0]+p[0], t[1]+p[1], t[2]+p[2]) in tiles:
                    black_ct += 1
                else:
                    white_adj_cts[(t[0]+p[0], t[1]+p[1], t[2]+p[2])].add((t[0], t[1], t[2]))
            if black_ct == 0 or black_ct > 2:
                next_white.add(t)
        for k, v in white_adj_cts.items():
            if len(v) == 2:
                next_black.add(k)
        
        for nb in next_black:
            tiles.add(nb)
        for nw in next_white:
            tiles.remove(nw)

    
    print(len(tiles))



def test_day_twenty_one():
    entries = utils.file_to_string_list("Day24sample.txt")
    run(entries)

def day_twenty_one():
    entries = utils.file_to_string_list("Day24.txt")
    run(entries)

if __name__=="__main__":
    test_day_twenty_one()
    day_twenty_one()
