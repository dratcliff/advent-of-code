def parse(filename):
    entries = []
    with open(filename) as f:
        for line in f:
            entries.append(line)
    return entries

"""A nice string is one with all of the following properties:

It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements."""

vowels = set(["a", "e", "i", "o", "u"])
bad_strings = set(["ab", "cd", "pq", "xy"])

def is_nice_string(s):
    vowel_ct = 0
    for c in s:
        if c in vowels:
            vowel_ct += 1

    twice = False
    bad = False

    for i, c in enumerate(s):
        if i  + 1 < len(s) and s[i+1] == c:
            twice = True
        if i + 1 < len(s) and s[i:i+2] in bad_strings:
            bad = True
    
    return vowel_ct >= 3 and twice and not bad


def day_five():
    assert True == is_nice_string("ugknbfddgicrmopn")
    assert True == is_nice_string("aaa")
    assert False == is_nice_string("jchzalrnumimnmhp")
    assert False == is_nice_string("haegwjzuvuyypxyu")
    assert False == is_nice_string("dvszwmarrgswjxmb")

    entries = parse("Day5.txt")
    ct = 0
    for e in entries:
        if is_nice_string(e):
            ct += 1
    assert 255 == ct


"""
Now, a nice string is one with all of the following properties:

It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
For example:

qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a letter that repeats with exactly one letter between them (zxz).
xxyxx is nice because it has a pair that appears twice and a letter that repeats with one between, even though the letters used by each rule overlap.
uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a single letter between them.
ieodomkazucvgmuy is naughty because it has a repeating letter with one between (odo), but no pair that appears twice.

"""

def is_nice_string2(s):
    rule_1 = False
    rule_2 = False
    for i in range(0, len(s)-1):
        if s.find(s[i:i+2], i+2) != -1:
            rule_1 = True
        if i < len(s) - 2 and s[i] == s[i+2]:
            rule_2 = True
    return rule_1 and rule_2

def day_five_part_two():
    assert True == is_nice_string2("qjhvhtzxzqqjkmpb")
    assert True == is_nice_string2("xxyxx")
    assert False == is_nice_string2("uurcxstgmygtbstg")
    assert False == is_nice_string2("ieodomkazucvgmuy")
    entries = parse("Day5.txt")
    ct = 0
    for e in entries:
        if is_nice_string2(e):
            ct += 1
    assert 55 == ct

if __name__=="__main__":
    day_five()
    day_five_part_two()