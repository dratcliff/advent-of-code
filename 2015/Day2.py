def parse(filename):
    entries = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\n')
            entries.append([int(x) for x in line.split("x")])
    return entries

def day_two():
    entries = parse("Day2.txt")
    entries = [[x[0]*x[1], x[1]*x[2], x[0]*x[2]] for x in entries]
    print(sum([min(e) + 2*sum(e) for e in entries]))

def day_two_part_two():
    entries = parse("Day2.txt")
    e2 = []
    for e in entries:
        p = 1
        p1 = []
        for e1 in e:
            p *= e1
            p1 = []
        p1.append(p)
        e.remove(max(e))
        for e1 in e:
            p1.append(2*e1)
        e2.append(p1)
    print(sum([sum(x) for x in e2]))

if __name__=="__main__":
    day_two()
    day_two_part_two()