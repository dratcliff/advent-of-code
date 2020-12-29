import sys
sys.path.append("../2020")
import utils.utils as utils

def tick(grid):
    """
    A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
    """
    next_grid = {}
    for y in grid:
        next_grid[y] = {}
        for x in grid[y]:
            ct = 0
            for yi in (y-1, y, y+1):
                if yi in grid:
                    ya = grid[yi]
                    for xi in (x-1, x, x+1):
                        if not (xi == x and yi == y):
                            if xi in ya:
                                if ya[xi] == "#":
                                    ct += 1
            if grid[y][x] == "#":
                if ct == 2 or ct == 3:
                    next_grid[y][x] = "#"
                else:
                    next_grid[y][x] = "."
            else:
                if ct == 3:
                    next_grid[y][x] = "#"
                else:
                    next_grid[y][x] = "."

    return next_grid

def test_day_eighteen():
    grid = utils.file_to_grid("Day18sample.txt")
    for i in range(0, 4):
        grid = tick(grid)
    
    s = 0
    for y in grid:
        for x in grid[y]:
            if grid[y][x] == "#":
                s += 1
    print(s)

def test_day_eighteen_part_two():
    grid = utils.file_to_grid("Day18sample.txt")
    grid[0][0] = "#"
    grid[0][5] = "#"
    grid[5][0] = "#"
    grid[5][5] = "#"
    for i in range(0, 5):
        grid = tick(grid)
        grid[0][0] = "#"
        grid[0][5] = "#"
        grid[5][0] = "#"
        grid[5][5] = "#"
    
    s = 0
    for y in grid:
        for x in grid[y]:
            if grid[y][x] == "#":
                s += 1
    print(s)

def day_eighteen():
    grid = utils.file_to_grid("Day18.txt")
    for i in range(0, 100):
        grid = tick(grid)
    
    s = 0
    for y in grid:
        for x in grid[y]:
            if grid[y][x] == "#":
                s += 1
    print(s)

def day_eighteen_part_two():
    grid = utils.file_to_grid("Day18.txt")
    grid[0][0] = "#"
    grid[0][99] = "#"
    grid[99][0] = "#"
    grid[99][99] = "#"
    for i in range(0, 100):
        grid = tick(grid)
        grid[0][0] = "#"
        grid[0][99] = "#"
        grid[99][0] = "#"
        grid[99][99] = "#"
    s = 0
    for y in grid:
        for x in grid[y]:
            if grid[y][x] == "#":
                s += 1
    print(s)

if __name__=="__main__":
    test_day_eighteen()
    day_eighteen()
    test_day_eighteen_part_two()
    day_eighteen_part_two()