
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
    # if m1.px > m2.px:
    #     m1.vx -= 1
    #     m2.vx += 1
    # elif m2.px > m1.px:
    #     m1.vx += 1
    #     m2.vx -= 1

    # if m1.py > m2.py:
    #     m1.vy -= 1
    #     m2.vy += 1
    # elif m2.py > m1.py:
    #     m1.vy += 1
    #     m2.vy -= 1

    # if m1.pz > m2.pz:
    #     m1.vz -= 1
    #     m2.vz += 1
    # elif m2.pz > m1.pz:
    #     m1.vz += 1
    #     m2.vz -= 1

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

print(total_energy_after(sample_one, 100))

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

# print(total_energy_after(part_one, 1000))

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
    m0 = {}
    m1 = {}
    m2 = {}
    m3 = {}
    found = False
    i = 0
    
    d = {}
    while not found:
        count = 0
        i = i + 1
        time_step(moons)
        for j in range(0, 4):
            if moons[j].v[2] == copy_moons[j].v[2] and moons[j].p[2] == copy_moons[j].p[2]:
                count += 1
        if count == 4:
            return i
        # d0 = np.array2string((np.array([moons[0].p, moons[0].v])))
        # d1 = np.array2string((np.array([moons[1].p, moons[1].v])))
        # d2 = np.array2string((np.array([moons[2].p, moons[2].v])))
        # d3 = np.array2string((np.array([moons[3].p, moons[3].v])))
       
            # exit()

        # if moons[0].v.all() == 0 and moons[1].v.all() == 0 and moons[2].v.all() == 0 and moons[3].v.all() == 0:
        #     sumx, sumy, sumz = 0, 0, 0
        #     for m in moons:
        #         print(m.p)
        #         sumx += m.p[0]
        #         sumy += m.p[1]
        #         sumz += m.p[2]
        #     print(sumx, sumy, sumz)

        # d0d1 = d0+d1

        # if d0d1 not in m0:
        #     m0[d0d1] = True
        # else:
        #     print("!!!")
        #     found = True

        # if d0 not in m0:
        #     m0[d0] = True
        # # else:
        #     # print(d0, "d0 what", i)
        
        # if d1 not in m1:
        #     m1[d1] = True
        # # else:
        #     # print(d1, "d1 what", i)

        # if d2 not in m2:
        #     m2[d2] = True
        # # else:
        #     # print(d2, "d2 what", i)

        # if d3 not in m3:
        #     m3[d3] = True
        # # else:
        #     # print(d3, "d3 what", i)
        
        # i += 1
        # print(m0[d0], m1[d1], m2[d2], m3[d3])
        if i % 10000000 == 0:
            print(i)
            found = True
        # te = system_energy(moons)
        # if te not in m:
            # m[te] = 1
        # else:
            # found = True
            # m[te].append(represent(moons))
            # if len(m[te]) > 1:
            #     for e in combinations(m[te], 2):
            #         e1 = e[0]
            #         e2 = e[1]
            #         if (e1[0] == e2[0] and 
            #                 e1[1] == e2[1] and
            #                 e1[2] == e2[2] and
            #                 e1[3] == e2[3]):    
            #             found = True
            #             print(e1[0].__dict__, e2[0].__dict__)
            #             print(e1[1].__dict__, e2[1].__dict__)
            #             print(e1[2].__dict__, e2[2].__dict__)
            #             print(e1[3].__dict__, e2[3].__dict__)
    return i

print(when_repeats(sample_one, _sample_one))

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

print(when_repeats(part_one, _part_one))

