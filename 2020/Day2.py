class Password:
    def __init__(self, required_char, required_occurs, password):
        self.required_char = required_char
        self.required_occurs = required_occurs
        self.password = password
        min_max = self.required_occurs.split('-')    
        self.min_occurs = int(min_max[0])
        self.max_occurs = int(min_max[1])
        self.first_position = self.min_occurs
        self.second_position = self.max_occurs

    def __str__(self):
        return self.required_char + "," + self.min_occurs + "-" + self.max_occurs + "," + self.password

    def __repr__(self):
        return self.required_char + "," + self.min_occurs + "-" + self.max_occurs + "," + self.password

def parse(filename):
    entries = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip('\n')
            line = line.replace(':', '')
            line = line.split(' ')
            entries.append(Password(line[1], line[0], line[2]))
    return entries

def count_valid(passwords):
    c = 0
    for p in passwords:
        occurs = p.password.count(p.required_char)
        if occurs >= p.min_occurs and occurs <= p.max_occurs:
            c += 1
    return c

def count_valid_2(passwords):
    c = 0
    for p in passwords:
        if (p.password[p.first_position-1] == p.required_char) != (p.password[p.second_position-1] == p.required_char):
            c += 1
    return c

def test_part_one():
    entries = parse("Day2sample.txt")
    c = count_valid(entries)
    assert 2 == c

def part_one():
    entries = parse("Day2.txt")
    c = count_valid(entries)
    assert 538 == c

def test_part_two():
    entries = parse("Day2sample.txt")
    c = count_valid_2(entries)
    assert 1 == c

def part_two():
    entries = parse("Day2.txt")
    c = count_valid_2(entries)
    assert 489 == c

if __name__=="__main__":
    test_part_one()
    part_one()
    test_part_two()
    part_two()