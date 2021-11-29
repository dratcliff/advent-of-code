import networkx as nx
from utils.utils import timed

def parse(filename):
    entries = []
    with open(filename) as f:
        for line in f:
            entries.append(int(line))
    return entries

def get_joltage_diffs(entries):
    entries = sorted(entries)
    entries.insert(0, 0)
    ones = 0
    twos = 0
    threes = 0
    for i in range(0, len(entries)-1):
        diff = entries[i+1] - entries[i]
        if diff == 1:
            ones += 1
        if diff == 2:
            twos += 1
        if diff == 3:
            threes += 1
    threes += 1 # for device's adapter

    return (ones, twos, threes)

def test_day_ten():
    entries = parse("Day10sample.txt")
    diffs = get_joltage_diffs(entries)
    assert 35 == diffs[0] * diffs[2]

    entries = parse("Day10sample2.txt")
    diffs = get_joltage_diffs(entries)
    assert 220 == diffs[0] * diffs[2]

def day_ten():
    entries = parse("Day10.txt")
    diffs = get_joltage_diffs(entries)
    assert 2738 == diffs[0] * diffs[2]

def count_options(G, cur, nxt):
    return sum([1 for x in nx.all_simple_paths(G, cur, nxt)]) 

def count_paths(entries):
    entries = sorted(entries)
    entries.insert(0, 0)
    entries.append(entries[-1]+3)

    G = nx.DiGraph()
    for i in entries:
        G.add_node(i)

    ones = 0
    twos = 0
    threes = 1
    mandatory = []

    for i in entries:
        if i+1 in entries:
            G.add_edge(i, i+1)
            ones += 1
        if i+2 in entries:
            G.add_edge(i, i+2)
            twos += 1
        if i+3 in entries:
            G.add_edge(i, i+3)
            threes += 1
            if i+2 not in entries and i+1 not in entries:
                    mandatory.append((i, i+3))

    ct = count_options(G, 0, mandatory[0][0])
    
    for i in range(0, len(mandatory) - 1):
        cur = mandatory[i]
        nxt = mandatory[i+1]
        if cur[1] != nxt[0]:
            ct *= count_options(G, cur[1], nxt[0])

    return ct

@timed
def test_day_ten_part_two():
    entries = parse("Day10sample.txt")
    assert 8 == count_paths(entries) #8

@timed
def test_day_ten_part_two_a():
    entries = parse("Day10sample2.txt")
    assert 19208 == count_paths(entries) #19208
    
@timed
def day_ten_part_two():
    entries = parse("Day10.txt")
    assert 74049191673856 == count_paths(entries)

if __name__=="__main__":
    test_day_ten()
    day_ten()
    test_day_ten_part_two()
    test_day_ten_part_two_a()
    day_ten_part_two()