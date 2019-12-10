from textwrap import dedent
from itertools import permutations
from math import gcd
from test_one import getLines

# top-left is 0,0
# immediately to right is 1,0

# for each asteroid, for each other asteroid, mark all positions it blocks

_e1_in = """.#..#
            .....
            #####
            ....#
            ...##"""
e1_in = [dedent(x) for x in _e1_in.split('\n')]

_e1_out = """.7..7
             .....
             67775
             ....7
             ...87"""

e1_out = [dedent(x) for x in _e1_out.split('\n')]

# for k, v in enumerate(e1_in):
#     for l, w in enumerate(v):
#         print(k, l, w)

def get_asteroids(input):
    m = {(k,l):w for k,v in enumerate(input) for l,w in enumerate(v)}
    return {k:v for k,v in m.items() if v=='#'}

def get_visible_counts(asteroids):
    m = {}
    for a, b in permutations(asteroids, 2):
        dx = a[0]-b[0]
        dy = a[1]-b[1]
        g = gcd(dx, dy)
        if a not in m:
            m[a] = []
        m[a].append((dx/g, dy/g))
    return [len(set(m[k])) for k in m]

def get_max(input):
    asteroids = get_asteroids(input)
    return max(get_visible_counts(asteroids))


# e1_map = {(k,l):w for k,v in enumerate(e1_in) for l,w in enumerate(v)}

# e1_asteroids = {k:v for k,v in e1_map.items() if v=='#'}

# m = {}
# for a, b in permutations(e1_asteroids, 2):
#     dx = a[0]-b[0]
#     dy = a[1]-b[1]
#     g = gcd(dx, dy)
#     if a not in m:
#         m[a] = []
#     m[a].append((dx/g, dy/g))
#     print(a, b, dx/g, dy/g, g)

print(get_max(e1_in))

_e2_in = """......#.#.
            #..#.#....
            ..#######.
            .#.#.###..
            .#..#.....
            ..#....#.#
            #..#....#.
            .##.#..###
            ##...#..#.
            .#....####"""
e2_in = [dedent(x) for x in _e2_in.split('\n')]

_e3_in = """.#..##.###...#######
            ##.############..##.
            .#.######.########.#
            .###.#######.####.#.
            #####.##.#.##.###.##
            ..#####..#.#########
            ####################
            #.####....###.#.#.##
            ##.#################
            #####.##.###..####..
            ..######..##.#######
            ####.##.####...##..#
            .#####..#.######.###
            ##...#.##########...
            #.##########.#######
            .####.#.###.###.#.##
            ....##.##.###..#####
            .#.#.###########.###
            #.#.#.#####.####.###
            ###.##.####.##.#..##"""

e3_in = [dedent(x) for x in _e3_in.split('\n')]

print(get_max(e2_in))
print(get_max(e3_in))

part_one = getLines('10.txt', to_int=False)
print(get_max(part_one))