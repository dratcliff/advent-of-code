import sys

sys.path.append("../2020/")

import utils
from itertools import permutations

def get_permutations():
    all = set()
    for i in range(0, 101):
        for j in range(0, 101-i):
            for k in range(0, 101-i-j):
                for l in range(0, 101-i-j-k):
                    if i + j + k + l == 100 and len(set([i,j,k,l])) == 4:
                        all.add((i,j,k,l))
    return all

def get_score(m, quantities):
    keys = list(m.keys())
    c = 0
    f = 0
    d = 0
    t = 0
    calories = 0
    for i in range(0, len(quantities)):
        k = keys[i]
        q = quantities[i]
        c += q*m[k]["capacity"]
        f += q*m[k]["flavor"]
        d += q*m[k]["durability"]
        t += q*m[k]["texture"]
        calories += q*m[k]["calories"]
        
    if c < 0 or f < 0 or d < 0 or t < 0:
        return 0
    #part two
    if calories != 500:
        return 0
    return c*f*d*t


def get_ingredients(entries):
    m = {}
    for e in entries:
        name = e.split(": ")[0]
        ingredients = e.split(": ")[1]
        ingredients = ingredients.split(", ")
        m2 = {}
        for i in ingredients:
            i = i.split(" ")
            m2[i[0]] = int(i[1])
        m[name] = m2
    return m

def test_day_fifteen():
    entries = utils.file_to_string_list("Day15sample.txt")
    m = get_ingredients(entries)
    # assert 62842880 == get_score(m, [44, 56])

def day_fifteen():
    entries = utils.file_to_string_list("Day15.txt")
    m = get_ingredients(entries)
    perms = get_permutations()

    best = 0
    for p in perms:
        s = get_score(m, p)
        if s > best:
            best = s
            print(s, m, p)
    

if __name__=="__main__":
    test_day_fifteen()
    day_fifteen()