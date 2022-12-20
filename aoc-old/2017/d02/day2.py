from utilaoc import file_to_strings

input = file_to_strings("day2input.txt")

input = [x.split("\t") for x in input]
input = [[int(x) for x in y] for y in input]

from itertools import combinations
s = 0
for i in input:
    for c in combinations(i, 2):
        if c[0] % c[1] == 0:
            s += c[0]//c[1]
        if c[1] % c[0] == 0:
            s += c[1]//c[0]

print(s)