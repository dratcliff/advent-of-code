def parse(filename):
    entries = []
    with open(filename) as f:
        entry = {}
        entries.append(entry)
        for line in f:
            if 1 == len(line):
                entry = {}
                entries.append(entry)
            else:
                line = line.strip('\n')
                fields = line.split(' ')
                for field in fields:
                    kv = field.split(':')
                    entry[kv[0]] = kv[1]
    return entries

def valid_cid(entry):
    field_ct = len(entry.keys())
    if field_ct == 8 or (field_ct == 7 and "cid" not in entry):
        return True
    return False

def valid_byr(entry):
    byr = entry["byr"]
    try:
        byr = int(byr)
    except:
        return False
    if 1920 <= byr <= 2002:
        return True
    return False

def valid_iyr(entry):
    iyr = entry["iyr"]
    try:
        iyr = int(iyr)
    except:
        return False
    if 2010 <= iyr <= 2020:
        return True
    return False

def valid_eyr(entry):
    eyr = entry["eyr"]
    try:
        eyr = int(eyr)
    except:
        return False
    if 2020 <= eyr <= 2030:
        return True
    return False

def valid_hgt(entry):
    hgt = entry["hgt"]
    if "cm" in hgt:
        hgt = hgt.replace("cm", "")
        hgt = int(hgt)
        if 150 <= hgt <= 193:
            return True
        else:
            return False
    elif "in" in hgt:
        hgt = hgt.replace("in", "")
        hgt = int(hgt)
        if 59 <= hgt <= 76:
            return True
        else:
            return False
    else:
        return False

def valid_hcl(entry):
    from re import search
    hcl = entry["hcl"]
    m = search(r"^\#[0-9a-f]{6}$", hcl)
    if m:
        return True
    return False

def valid_ecl(entry):
    ecl = entry["ecl"]
    if ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return True
    return False

def valid_pid(entry):
    pid = entry["pid"]
    from re import search
    m = search(r"^[0-9]{9}$", pid)
    if m:
        return True
    return False

def count_valid(entries):
    ct = 0
    for entry in entries:
        l = len(entry.keys())
        if l == 8 or (l == 7 and "cid" not in entry.keys()):
                ct += 1
    return ct

def count_valid2(entries):
    """
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.
    """
    ct = 0
    for entry in entries:
        if valid_cid(entry) and valid_byr(entry) and valid_iyr(entry) and valid_eyr(entry) \
            and valid_hgt(entry) and valid_hcl(entry) and valid_ecl(entry) and valid_pid(entry):
                ct += 1
    return ct

def day_four():
    entries = parse("Day4.txt")
    ct = count_valid(entries)
    assert 170 == ct

def test_day_four():
    entries = parse("Day4sample.txt")
    ct = count_valid(entries)
    assert 2 == ct

def day_four_part_two():
    entries = parse("Day4.txt")
    ct = count_valid2(entries)
    assert 103 == ct

if __name__=="__main__":
    test_day_four()
    day_four()
    day_four_part_two()