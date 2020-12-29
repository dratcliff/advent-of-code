def parse(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            lines.append(line)
    return lines

def day_one():
    lines = parse("Day1.txt")
    floor = 0
    i = 0
    line = lines[0]
    for c in line:
        i += 1
        if c == "(":
            floor += 1
        elif c == ")":
            floor -= 1
        if floor == -1:
            print("basement", i)

    print("final", floor)



if __name__=="__main__":
    day_one()