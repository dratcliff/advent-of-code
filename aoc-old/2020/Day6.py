def parse(filename):
    entries = []
    group = {}
    group["ct"] = 0
    entries.append(group)
    with open(filename) as f:
        for line in f:
            line = line.strip('\n')
            if len(line) == 0:
                group = {}
                group["ct"] = 0
                entries.append(group)
            else:
                group["ct"] += 1
            for i in line:
                if i in group:
                    group[i] += 1
                else:
                    group[i] = 1
    return entries

def check(entries):
    total = 0
    for e in entries:
        ct = e["ct"]
        for k in e:
            if k != "ct":
                if e[k] == ct:
                    total += 1
    return total

def test_day_six():
    entries = parse("Day6sample.txt")
    total = check(entries)
    assert 6 == total

def day_six():
    entries = parse("Day6.txt")
    total = check(entries)
    print(total)

if __name__=="__main__":
    test_day_six()
    day_six()