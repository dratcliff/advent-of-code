from textwrap import dedent
from itertools import permutations
from math import gcd
from test_one import getLines

def get_asteroids(input):
    m = {(l,k):w for k,v in enumerate(input) for l,w in enumerate(v)}
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
    return [(k, len(set(m[k]))) for k in m]

def get_max(input):
    asteroids = get_asteroids(input)
    return max(get_visible_counts(asteroids), key=lambda x: x[1])

def test_one():
    _e1_in = """.#..#
                .....
                #####
                ....#
                ...##"""
    e1_in = [dedent(x) for x in _e1_in.split('\n')]
    assert get_max(e1_in) == ((3,4), 8)

def test_two():
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
    assert get_max(e2_in) == ((5,8), 33)

def test_three():
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
    assert get_max(e3_in) == ((11,13), 210)

def test_part_one():
    part_one = getLines('10.txt', to_int=False)
    assert get_max(part_one) == ((20, 18), 280) 