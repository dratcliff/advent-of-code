import sys
sys.path.append("../2020")

import utils.utils as utils

replacements = {}
unreplacements = {}
def populate(entries):
    starting = ""
    for e in entries:
        if "=>" in e:
            e = e.split(" => ")
            if e[0] not in replacements:
                replacements[e[0]] = set()
            if e[1] not in unreplacements:
                unreplacements[e[1]] = e[0]
            else:
                raise Exception("OMG", e[0], unreplacements[e[1]], e[1])
            replacements[e[0]].add(e[1])
        else:
            e = e.strip('\n')
            if len(e) > 0:
                starting = e
    return starting

dp = {}
def replace(starting):
    if starting in dp:
        return dp[starting]
    all = set()
    i = 0
    while i < len(starting):
        cur = starting[i]
        after = starting[i+1:]
        before = starting[:i]
        if cur not in replacements:
            cur = starting[i:i+2]
            after = starting[i+2:]
        if cur not in replacements:
            i += 1
            continue
        for v in replacements[cur]:
            all.add(before + v + after)
        i += 1
    dp[starting] = all
    return all

def unreplace(starting):
    all = set()
    i = 0
    for k in unreplacements.keys():
        if "Ar" in k:
            i = starting.find(k)
            while i != -1:
                all.add(starting.replace(k, unreplacements[k]))
                i = starting.find(k, i+1)
    return all

def test_day_nineteen():
    entries = utils.file_to_string_list("Day19.txt")
    starting = populate(entries)
    d = replace(starting)
    print(len(replacements))
    assert 535 == len(d)

def test_day_nineteen_part_two():
    entries = utils.file_to_string_list("Day19.txt")
    starting = populate(entries)
    all = set()
    all.add("e")
    for i in range(0, 10):
        new = set()
        for a in all:
            new2 = replace(a)
            for n in new2:
                new.add(n)
        for n in new:
            if n[-2:] != "Ar":
                all.add(n)
    print(len(all))

if __name__=="__main__":
    # test_day_nineteen()
    test_day_nineteen_part_two()