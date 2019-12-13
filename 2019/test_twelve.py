
from itertools import permutations, combinations
from copy import deepcopy
from math import copysign
import numpy as np

"""
To apply gravity, consider every pair of moons. On each axis (x, y, and z), 
the velocity of each moon changes by exactly +1 or -1 to pull the moons together. 
For example, if Ganymede has an x position of 3, and Callisto has a x position
of 5, then Ganymede's x velocity changes by +1 (because 5 > 3) and Callisto's x 
velocity changes by -1 (because 3 < 5). However, if the positions on a given 
axis are the same, the velocity on that axis does not change for that pair of moons.

Once all gravity has been applied, apply velocity: simply add the velocity of 
each moon to its own position. For example, if Europa has a position of x=1, y=2, z=3 
and a velocity of x=-2, y=0,z=3, then its new position would be x=-1, y=2, z=6. This
process does not modify the velocity of any moon.
"""

""" sample one
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""

class Moon:
    def __init__(self, x=0, y=0, z=0):
        self.p = np.array([x, y, z])
        self.v = np.array([0, 0, 0])

    def __eq__(self, other):
        if not isinstance(other, Moon):
            return NotImplemented
        return self.v == other.p and self.v == other.v

sample_one = [
    Moon(x=-1, y=0, z=2),
    Moon(x=2, y=-10, z=-7),
    Moon(x=4, y=-8, z=8),
    Moon(x=3, y=5, z=-1)
]

from math import gcd
def lcm(a):
    lcm = a[0]
    for i in a[1:]:
        lcm = int(lcm*i/gcd(lcm, i))
    return lcm

def apply_gravity(moon_tuple):
    m1 = moon_tuple[0]
    m2 = moon_tuple[1]

    dp = np.sign(m1.p-m2.p)
    m1.v -= dp
    m2.v += dp

def apply_velocity(moon):
    # print(moon.p)
    moon.p += moon.v

def get_combinations(moons):
    return combinations(moons, 2)

def time_step(moons):
    for x in get_combinations(moons):
        apply_gravity(x)

    for x in moons:
        apply_velocity(x)
    

def total_energy(moon):
    return sum(abs(moon.p))*sum(abs(moon.v))

def system_energy(moons):
    sum = 0
    for moon in moons:
        sum += total_energy(moon)
    return sum

def total_energy_after(moons, no_steps):
    for i in range(0, no_steps):
        time_step(moons)

    sum = 0
    for x in moons:
        sum += total_energy(x)

    return sum

""" input for part one, probably not worth writing parser
<x=6, y=10, z=10>
<x=-9, y=3, z=17>
<x=9, y=-4, z=14>
<x=4, y=14, z=4>"""

part_one = [
    Moon(x=6, y=10, z=10),
    Moon(x=-9, y=3, z=17),
    Moon(x=9, y=-4, z=14),
    Moon(x=4, y=14, z=4)
]

def test_part_one():
    part_one = [
        Moon(x=6, y=10, z=10),
        Moon(x=-9, y=3, z=17),
        Moon(x=9, y=-4, z=14),
        Moon(x=4, y=14, z=4)
    ]
    result = total_energy_after(part_one, 1000)
    assert result == 13045

sample_one = [
    Moon(x=-1, y=0, z=2),
    Moon(x=2, y=-10, z=-7),
    Moon(x=4, y=-8, z=8),
    Moon(x=3, y=5, z=-1)
]

_sample_one = [
    Moon(x=-1, y=0, z=2),
    Moon(x=2, y=-10, z=-7),
    Moon(x=4, y=-8, z=8),
    Moon(x=3, y=5, z=-1)
]

def when_repeats(moons, copy_moons):
    found = False
    i = 0
    d = {}
    while not found:
        count = 0
        i = i + 1
        time_step(moons)
        for k in range(0, 3):
            fixed = {}
            for j in range(0, 4):
                if moons[j].v[k] == copy_moons[j].v[k] and moons[j].p[k] == copy_moons[j].p[k]:
                    if j not in fixed:
                        fixed[j] = i
            if len(fixed) == 4:
                d[k] = i
        if len(d) == 3:
            return d
        if i % 10000000 == 0:
            print(i)
            found = True
    return d

def test_part_two_sample():
    cycle_by_axis = when_repeats(sample_one, _sample_one).values()
    result = lcm(list(cycle_by_axis))
    assert result == 2772

part_one = [
    Moon(x=6, y=10, z=10),
    Moon(x=-9, y=3, z=17),
    Moon(x=9, y=-4, z=14),
    Moon(x=4, y=14, z=4)
]

_part_one = [
    Moon(x=6, y=10, z=10),
    Moon(x=-9, y=3, z=17),
    Moon(x=9, y=-4, z=14),
    Moon(x=4, y=14, z=4)
]

def test_part_two():
    cycle_by_axis = when_repeats(part_one, _part_one).values()
    result = lcm(list(cycle_by_axis))
    assert result == 344724687853944

