class Bag:
    def __init__(self, contents):
        self.contents = []
        for c in contents.split(','):
            c = c.rstrip('.')
            c = c.rstrip(' ')
            c = c.lstrip(' ')
            if c != "no other":
                self.contents.append({c[2:]: int(c[0])})


    def __str__(self):
        return str(self.contents)

    def __repr__(self):
        return str(self.contents)

    def has_contents(self):
        return len(self.contents) > 0

def parse(filename):
    entries = {}
    with open(filename) as f:
        for line in f:
            line = line.strip('\n')
            line = line.replace("bags", "")
            line = line.replace("bag", "")
            entry = line.split("contain")
            k = entry[0].rstrip(' ')
            entries[k] = Bag(entry[1])
    return entries


def check_all(entries):
    contains_shiny_gold = set()
    for k, v in entries.items():
        if shiny_gold(entries, k, v, False) and k != "shiny gold":
            contains_shiny_gold.add(k)
    return len(contains_shiny_gold)

def shiny_gold(entries, k, v, contains_shiny_gold):
    if k == "shiny gold":
        contains_shiny_gold = True
    if v.has_contents():
        for e in v.contents:
            for k1, v1 in e.items():
                contains_shiny_gold = shiny_gold(entries, k1, entries[k1], contains_shiny_gold)
    return contains_shiny_gold

def test_day_seven():
    entries = parse("Day7sample.txt")
    assert 4 == check_all(entries)

def count_bags(entries, bag_color):
    contents = entries[bag_color].contents
    ct = 0
    for c in contents:
        for k in c.keys():
            child_contents = entries[k].contents
            if len(child_contents) == 0:
                ct += c[k]
            else:
                ct += c[k] + c[k] * count_bags(entries, k)
    return ct
    

def check_all2(entries):
    ct = count_bags(entries, "shiny gold")
    return ct


def test_day_seven_part_two():
    entries = parse("Day7sample.txt")
    check_all2(entries)
    entries = parse("Day7sample2.txt")
    check_all2(entries)

def day_seven():
    entries = parse("Day7.txt")
    assert 335 == check_all(entries)

def day_seven_part_two():
    entries = parse("Day7.txt")
    assert 2431 == check_all2(entries)

if __name__=="__main__":
    test_day_seven()
    day_seven()
    test_day_seven_part_two()
    day_seven_part_two()