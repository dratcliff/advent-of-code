"""
"" is 2 characters of code (the two double quotes), but the string contains zero characters.
"abc" is 5 characters of code, but 3 characters in the string data.
"aaa\"aaa" is 10 characters of code, but the string itself contains six "a" characters and a single, escaped quote character, for a total of 7 characters in the string data.
"\x27" is 6 characters of code, but the string itself contains just one - an apostrophe ('), escaped using hexadecimal notation.
"""
import re

def parse(filename):
    entries = []
    with open(filename) as f:
        for line in f:
            entries.append(line.rstrip('\n'))
    return entries

def count(s):
    code_ct = len(s)
    s2 = s[1:-1]
    code_ct -= 2
    code_ct -= s2.count("\\\\")
    code_ct -= s2.count("\\\"")
    code_ct -= len(re.findall(r"\\x[0-9a-f]{2}", s2))*3
    return len(s) - code_ct

def part_two(s):
    ct = len(s)
    ct += s.count("\\")
    ct += s.count("\"")
    ct += 2
    return ct - len(s)

def day_eight():
    entries = parse("Day8.txt")
    ct = 0
    ct2 = 0
    for e in entries:
        ct += count(e)
        ct2 += part_two(e)
    assert 1371 == ct   
    print(ct2)


if __name__=="__main__":
    day_eight()