from textwrap import dedent
from itertools import permutations, groupby
from operator import itemgetter, attrgetter
from math import gcd, atan2, pi, hypot
from test_one import getLines


def get_asteroids(input):
    m = {(l, k): w for k, v in enumerate(input) for l, w in enumerate(v)}
    return {k: v for k, v in m.items() if v == '#'}


def get_angle(tuple):
    angle = atan2(1, 0) - atan2(tuple[1], tuple[0])
    if angle < 0:
        angle = angle + 2*pi
    return angle, hypot(tuple[2][0]-11, tuple[2][1]-13)


class AsteroidDistance:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.fromx = 0
        self.fromy = 0
        self.tox = 0
        self.toy = 0
        self.angle = 0
        self.length = 0

    def as_dict(self):
        return self.__dict__


def distances(asteroids):
    m = {}
    for a, b in permutations(asteroids, 2):
        dx = b[0]-a[0]
        dy = a[1]-b[1]
        g = gcd(dx, dy)
        h = hypot(dx, dy)
        if a not in m:
            m[a] = []
        ad = AsteroidDistance()
        ad.dx = dx/g
        ad.dy = dy/g
        ad.tox = b[0]
        ad.toy = b[1]
        ad.fromx = a[0]
        ad.fromy = a[1]
        ad.angle = get_angle((dx, dy, b))[0]
        ad.length = get_angle((dx, dy, b))[1]

        m[a].append(ad)
    return m


def get_visible_counts(asteroids):
    m = distances(asteroids)
    return [(k, len(set([x.angle for x in m[k]]))) for k in m]


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
    print(get_max(e1_in))
    assert get_max(e1_in) == ((3, 4), 8)


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
    assert get_max(e2_in) == ((5, 8), 33)


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
    assert get_max(e3_in) == ((11, 13), 210)


def test_part_one():
    part_one = getLines('resources/10.txt', to_int=False)
    assert get_max(part_one) == ((20, 18), 280)


def accumulate(l):
    groups = []
    it = groupby(l, attrgetter('angle'))
    for key, subiter in it:
        groups.append(list(subiter))
    return groups


def rotate_laser(distances_by_angle):
    result = []
    d = distances_by_angle
    while len(d) > 0:
        for k in d:
            if len(k) > 0:
                result.append(k.pop(0))
            else:
                d.remove(k)
    return result


def test_part_two():
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
    a = get_asteroids(e3_in)
    d = distances(a)
    m = get_max(e3_in)
    t = d[m[0]]
    s = sorted(t, key=attrgetter('angle', 'length'))
    by_angle = accumulate(s)
    rotated = rotate_laser(by_angle)

    """
    The 1st asteroid to be vaporized is at 11,12.
    The 2nd asteroid to be vaporized is at 12,1.
    The 3rd asteroid to be vaporized is at 12,2.
    The 10th asteroid to be vaporized is at 12,8.
    The 20th asteroid to be vaporized is at 16,0.
    The 50th asteroid to be vaporized is at 16,9.
    The 100th asteroid to be vaporized is at 10,16.
    The 199th asteroid to be vaporized is at 9,6.
    The 200th asteroid to be vaporized is at 8,2.
    The 201st asteroid to be vaporized is at 10,9.
    The 299th and final asteroid to be vaporized is at 11,1.
    """
    assert (rotated[0].tox == 11 and rotated[0].toy == 12)
    assert (rotated[1].tox == 12 and rotated[1].toy == 1)
    assert (rotated[2].tox == 12 and rotated[2].toy == 2)
    assert (rotated[9].tox == 12 and rotated[9].toy == 8)
    assert (rotated[19].tox == 16 and rotated[19].toy == 0)
    assert (rotated[49].tox == 16 and rotated[49].toy == 9)
    assert (rotated[99].tox == 10 and rotated[99].toy == 16)
    assert (rotated[198].tox == 9 and rotated[198].toy == 6)
    assert (rotated[199].tox == 8 and rotated[199].toy == 2)
    assert (rotated[200].tox == 10 and rotated[200].toy == 9)
    assert (rotated[298].tox == 11 and rotated[298].toy == 1)


def test_part_two_file():
    a = get_asteroids(getLines('resources/10.txt', to_int=False))
    d = distances(a)
    t = d[(20, 18)]

    s = sorted(t, key=attrgetter('angle', 'length'))
    abc = accumulate(s)
    result = rotate_laser(abc)

    assert (result[199].tox == 7 and result[199].toy == 6)
