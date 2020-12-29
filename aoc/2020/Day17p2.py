import utils.utils as utils
import itertools
my_set = set()
for i in itertools.permutations([-1, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 1], 4):
    my_set.add(i)
my_set.remove((0, 0, 0, 0))

def make_cube(grid, estimated_size):
    cube = {0: {}    }

    for y in grid:
        if y not in cube[0]:
            cube[0][y] = {}
        for x in grid[y]:
            if x not in cube[0][y]:
                cube[0][y][x] = {}
            cube[0][y][x][0] = grid[y][x]

    
    for z in range(-1*estimated_size, estimated_size):
        if z not in cube:
            cube[z] = {}
        for y in range(-1*estimated_size, estimated_size):
            if y not in cube[z]:
                cube[z][y] = {}
            for x in range(-1*estimated_size, estimated_size):
                if x not in cube[z][y]:
                    cube[z][y][x] = {}
                for w in range(-1*estimated_size, estimated_size):
                    if w not in cube[z][y][x]:
                        cube[z][y][x][w] = '.'
    
    
    return cube

def run(grid, cycles):
    cube = make_cube(grid, len(grid)+cycles+1)

    for i in range(cycles):
        turn_off = set()
        turn_on = set()
        for z in cube:
            for y in cube[z]:
                for x in cube[z][y]:
                    for w in cube[z][y][x]:
                        on_neighbors = 0
                        is_on = (cube[z][y][x][w] == '#')
                        for offsets in my_set:
                            zoff = z+offsets[0]
                            yoff = y+offsets[1]
                            xoff = x+offsets[2]
                            woff = w+offsets[3]
                            if zoff in cube and yoff in cube[zoff] and xoff in cube[zoff][yoff] and woff in cube[zoff][yoff][xoff]:
                                if cube[zoff][yoff][xoff][woff] == '#':
                                    on_neighbors += 1
                        if on_neighbors not in (2, 3) and is_on:
                            turn_off.add((z, y, x, w))
                            """
                            If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
                            If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
                            """
                        if not is_on and on_neighbors == 3:
                            turn_on.add((z, y, x, w))
        for o in turn_off:
            cube[o[0]][o[1]][o[2]][o[3]] = '.'
        for o in turn_on:
            cube[o[0]][o[1]][o[2]][o[3]] = '#'

    s = 0

    for z in cube:
        for y in cube[z]:
            for x in cube[z][y]:
                for w in cube[z][y][x]:
                    if cube[z][y][x][w] == '#':
                        s += 1
    
    print(s)


def test_day_seventeen():
    entries = utils.file_to_grid("Day17sample.txt")
    run(entries, 6)


def day_seventeen():
    entries = utils.file_to_grid("Day17.txt")
    run(entries, 6)

if __name__=="__main__":
    test_day_seventeen()
    day_seventeen()