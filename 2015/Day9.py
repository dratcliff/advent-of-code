from itertools import permutations

def parse(filename):
    entries = {}
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\n')
            e = line.split(" ")
            start = e[0]
            end = e[2]
            distance = int(e[4])
            if start not in entries:
                entries[start] = {}
            entries[start][end] = distance
            if end not in entries:
                entries[end] = {}
            entries[end][start] = distance

    return entries

def day_nine():
    entries = parse("Day9.txt")
    distances = set()
    for c in permutations(entries.keys(), len(entries.keys())):
        distance = 0
        for i in range(0, len(c)-1):
            distance += entries[c[i]][c[i+1]]
        distances.add(distance)
    assert min(distances) == 207
    assert max(distances) == 804

if __name__=="__main__":
    day_nine()