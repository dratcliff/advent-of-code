from utilaoc import file_to_integer_grid


"""
First, the energy level of each octopus increases by 1.
Then, any octopus with an energy level greater than 9 flashes. 
This increases the energy level of all adjacent octopuses by 1, 
including octopuses that are diagonally adjacent. If this 
causes an octopus to have an energy level greater than 9, it also flashes. 
This process continues as long as new octopuses keep having their 
energy level increased beyond 9. (An octopus can only flash at most once per step.)
Finally, any octopus that flashed during this step has its energy 
level set to 0, as it used all of its energy to flash.
"""

actual = file_to_integer_grid("a.txt")


def advance(grid):
    offsets = [
        (0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]
    for k in grid:
        grid[k] += 1
    flashing = True
    to_flash = set()
    flashed = set()
    while flashing:
        flashing = False
        for k in grid:
            if grid[k] > 9:
                if k not in flashed:
                    to_flash.add(k)
                    flashing = True
        while to_flash:
            f = list(to_flash)[0]
            for o in offsets:
                if (f[0]+o[0], f[1]+o[1]) in grid:
                    grid[(f[0]+o[0], f[1]+o[1])] += 1
                    flashed.add(f)
            to_flash.remove(f)
    res = False
    if len(flashed) == 100:
        res = True
    for f in flashed:
        grid[f] = 0
    return res


stop = False
i = 0
while not stop:
    i += 1
    stop = advance(actual)

print(i)
