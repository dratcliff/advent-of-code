from test_one import getLines
from math import pow

def tick(grid):
    """
        A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
        An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
    """
    for i in range(0, 1):
        new_grid = {}
        for k, v in grid.items():
            up = (k[0], k[1]-1)
            down = (k[0], k[1]+1)
            left = (k[0]-1, k[1])
            right = (k[0]+1, k[1])

            adj_bugs = 0

            if up in grid and grid[up] == "#":
                adj_bugs += 1
            if down in grid and grid[down] == "#":
                adj_bugs += 1
            if left in grid and grid[left] == "#":
                adj_bugs += 1
            if right in grid and grid[right] == "#":
                adj_bugs += 1

            if v == ".":
                if adj_bugs in (1, 2):
                    new_grid[k] = "#"
                else:
                    new_grid[k] = "."
            else:
                if adj_bugs == 1:
                    new_grid[k] = "#"
                else:
                    new_grid[k] = "."
    return new_grid

def bd_rating(grid):
    rating = 0
    for k, v in grid.items():
        if v == "#":
            i = k[1]*5 + k[0]
            rating = rating + int(pow(2, i))
    return rating

lines = getLines("resources/24.txt", to_int=False)
grid = {(j, i): w for i, v in enumerate(lines) for j, w in enumerate(v)}

ratings = {}
for i in range(0, 100):
    rating = bd_rating(grid)
    if rating not in ratings:
        ratings[rating] = True
        grid = tick(grid)
    else:
        print("twice", rating)
        break
        