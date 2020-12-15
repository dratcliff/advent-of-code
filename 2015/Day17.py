import sys

sys.path.append("../2020")

import utils

from itertools import combinations

def check(entries):
    combos = []
    for i in range(0, len(entries)):
        for e in combinations(entries, len(entries)-i):
            if sum(e) == 150:
                combos.append(e)
    print(min(len(c) for c in combos))
    print(sum(1 for c in combos if len(c) == 4))

def day_seventeen():
    entries = utils.file_to_int_list("Day17.txt")
    # check([20, 15, 10, 5, 5])
    check(entries)

if __name__=="__main__":
    day_seventeen()