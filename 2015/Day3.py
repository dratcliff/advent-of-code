def parse(filename):
    entries = []
    with open(filename) as f:
        for line in f:
            entries.append(line)
    return entries[0]

def count_houses(directions):
    x = 0
    y = 0
    visited = set()
    visited.add((0, 0))
    for d in directions:
        if d == "<":
            x -= 1
        elif d == ">":
            x += 1
        elif d == "v":
            y -= 1
        elif d == "^":
            y += 1
        visited.add((x, y))
    return len(visited)

def count_houses2(directions):
    x = 0
    y = 0
    other_x = 0
    other_y = 0
    visited = set()
    visited.add((0, 0))
    i = 0
    for d in directions:
        if d == "<":
            if i % 2 == 0:
                x -= 1
            else:
                other_x -= 1
        elif d == ">":
            if i % 2 == 0:
                x += 1
            else:
                other_x += 1
        elif d == "v":
            if i % 2 == 0:
                y -= 1
            else:
                other_y -= 1
        elif d == "^":
            if i % 2 == 0:
                y += 1
            else:
                other_y += 1
        visited.add((x, y))
        visited.add((other_x, other_y))
        i += 1
    return len(visited)

def day_three():
    entries = parse("Day3.txt")
    assert 2565 == count_houses(entries)

def day_three_part_two():
    entries = parse("Day3.txt")
    assert 2639 == count_houses2(entries)

if __name__=="__main__":
    day_three()
    day_three_part_two()