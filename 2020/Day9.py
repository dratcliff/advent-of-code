from itertools import combinations
from utils import timed

def parse(filename):
    entries = []
    with open(filename) as f:
        for line in f:
            entries.append(int(line.strip('\n')))
    return entries


def check(entries, preamble_len):
    for i in range(preamble_len, len(entries)):
        valid = False
        for c in combinations(entries[i-preamble_len:i], 2):
            if sum(c) == entries[i]:
                valid = True
                break
        if not valid:
            return entries[i]

def find_contig(entries, desired):
    found = False
    range_size = 2
    
    while not found:
        for i in range(0, len(entries)):
            if sum(entries[i:i+range_size]) == desired:
                found = True
                return entries[i:i+range_size]
        range_size += 1

@timed
def test_day_nine():
    entries = parse("Day9sample.txt")
    result = check(entries, 5)
    assert result == 127

@timed
def day_nine():
    entries = parse("Day9.txt")
    result = check(entries, 25)
    assert result == 375054920

@timed
def test_day_nine_part_two():
    entries = parse("Day9sample.txt")
    result = check(entries, 5)

    contig = find_contig(entries, result)
    result = min(contig) + max(contig)
    assert result == 62

@timed
def day_nine_part_two():
    entries = parse("Day9.txt")
    result = check(entries, 25)

    contig = find_contig(entries, result)
    result = min(contig) + max(contig)
    assert result == 54142584

if __name__=="__main__":
    test_day_nine()
    day_nine()
    test_day_nine_part_two()
    day_nine_part_two()