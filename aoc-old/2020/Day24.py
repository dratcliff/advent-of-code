import utils.utils as utils
from collections import defaultdict

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
