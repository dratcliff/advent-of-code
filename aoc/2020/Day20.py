import utils.utils as utils
import numpy as np
import pickle
from itertools import permutations
import re


class Images:
    def __init__(self, grid, adjacents):
        self.size = 0
        for k in grid:
            self.size += 1
        self.grid = grid
        self.adjacents = adjacents
        corners = []
        for a in adjacents:
            if len(adjacents[a]) == 2:
                corners.append(a)
        self.corners = corners
        self.arranged = {}
        starting_corner = None
        while starting_corner is None:
            for c in corners:
                for p in permutations(adjacents[c], 2):
                    left = grid[c]
                    right = grid[p[0]]
                    under = grid[p[1]]
                    left, right = align_left_right_corner(left, right)
                    under = align_under_top_fixed(left, under)
                    if under is not None:
                        starting_corner = left
                        self.arranged[(0, 0)] = (c, left)
                        self.arranged[(0, 1)] = (p[1], under)
                        self.arranged[(1, 0)] = (p[0], right)
                        self.arranged_size = 3

        for x in range(0, 12):
            for y in range(0, 12):
                self.arrange((x, y))

    def arrange(self, coord):
        tile_id, img_array = self.arranged[coord]
        above_coord = (coord[0], coord[1]-1)
        below_coord = (coord[0], coord[1]+1)
        left_coord = (coord[0]-1, coord[1])
        right_coord = (coord[0]+1, coord[1])
        adj = self.adjacents[tile_id]
        above_id = None
        left_id = None
        found_under = False
        found_right = False
        if coord[1] == 11:
            found_under = True
        if coord[0] == 11:
            found_right = True

        if above_coord in self.arranged:
            above_id = self.arranged[above_coord][0]
            adj.remove(above_id)
        if left_coord in self.arranged:
            left_id = self.arranged[left_coord][0]
            adj.remove(left_id)
        if below_coord in self.arranged:
            below_id = self.arranged[below_coord][0]
            adj.remove(below_id)
            found_under = True
        if right_coord in self.arranged:
            right_id = self.arranged[right_coord][0]
            adj.remove(right_id)
            found_right = True
        for a in adj:
            right = align_right_left_fixed(img_array, self.grid[a])
            if right is not None:
                found_right = True
                self.arranged[right_coord] = (a, right)
            under = align_under_top_fixed(img_array, self.grid[a])
            if under is not None:
                found_under = True
                self.arranged[below_coord] = (a, under)
        if not found_right or not found_under:
            raise Exception("Something went wrong")

    def remove_borders(self):
        for coord in self.arranged:
            tile_id, img_array = self.arranged[coord]
            img_array = np.delete(img_array, 9, 0)
            img_array = np.delete(img_array, 0, 0)
            img_array = np.delete(img_array, 9, 1)
            img_array = np.delete(img_array, 0, 1)
            self.arranged[coord] = (tile_id, img_array)

    def count_sea_monsters(self):
        rows = []
        for i in range(12):
            test = [k for k in self.arranged if k[1] == i]
            test = tuple(self.arranged[k][1] for k in test)
            row0 = np.concatenate(test, axis=1)
            rows.append(row0)
        matrix = np.concatenate(tuple(rows), axis=0)
        for i in range(0, 2):
            matrix = np.flip(matrix, axis=0)
            for j in range(0, 2):
                matrix = np.flip(matrix, axis=1)
                for k in range(0, 4):
                    matrix = np.rot90(matrix)
                    as_list = matrix.tolist()
                    strings = []
                    the_sum = 0
                    for row in as_list:
                        the_sum += sum(1 for x in row if x == 1)
                        row = ["#" if r == 1 else "." for r in row]
                        strings.append(''.join(row))

                    total_hashes = 0
                    sea_monster_count = 0
                    for i in range(0, len(strings)):
                        s = strings[i]
                        above = ""
                        if i > 0:
                            above = strings[i-1]
                        below = ""
                        if i < len(s)-1:
                            below = strings[i+1]
                        total_hashes += s.count("#")

                        for g in re.finditer(r'(?=(#....##....##....###))', s):
                            if i > 0 and i < len(strings)-1:
                                for h in re.finditer(r'(?=(.#..#..#..#..#..#...))', below):
                                    for w in re.finditer(r'(?=(..................#.))', above):
                                        if g.span()[0] == h.span()[0] and h.span()[0] == w.span()[0]:
                                            sea_monster_count += 1

                    if sea_monster_count > 0:
                        return sea_monster_count, total_hashes
        return 0


def align_left_right_corner(left, right):
    for q in range(0, 2):
        left = np.flip(left, 1)
        for r in range(0, 4):
            left = np.rot90(left)
            for i in range(0, 2):
                right = np.flip(right, 1)
                for j in range(0, 4):
                    right = np.rot90(right)
                    if np.all(np.equal(left[:, 9], right[:, 0])):
                        return left, right
    return None


def align_under_top_fixed(top, bottom):
    for i in range(0, 2):
        bottom = np.flip(bottom, 1)
        for j in range(0, 4):
            bottom = np.rot90(bottom)
            if np.all(np.equal(top[9], bottom[0])):
                return bottom
    return None


def align_right_left_fixed(left, right):
    for i in range(0, 2):
        right = np.flip(right, 1)
        for j in range(0, 4):
            right = np.rot90(right)
            if np.all(np.equal(left[:, 9], right[:, 0])):
                return right
    return None


def parse(filename):
    grids = {}
    entries = utils.file_to_string_list(filename)
    grid, id = None, None
    for e in entries:
        if "Tile" in e:
            if grid and id:
                grids[id] = np.array(grid)
            id = e.split(" ")[1]
            id = id.replace(":", "")
            grids[id] = []
            grid = []
        elif len(e) > 0:
            e = [1 if e == "#" else 0 for e in e]
            grid.append(list(e))
    grids[id] = np.array(grid)
    return grids


def get_adjacents(grid):
    adjacents = {}

    for k, v in grid.items():
        print(k)
        if k not in adjacents:
            adjacents[k] = set()
        for n, u in grid.items():
            if n not in adjacents:
                adjacents[n] = set()
            if k != n:
                for z in range(0, 2):
                    v = np.flip(v, 1)
                    for i in range(0, 4):
                        v = np.rot90(v)
                        for y in range(0, 2):
                            u = np.flip(u, 1)
                            for j in range(0, 4):
                                u = np.rot90(u)
                                if np.all(np.equal(v[9], u[0])):
                                    adjacents[k].add(n)
                                    adjacents[n].add(k)

    return adjacents


def get_corners(grid):
    adjacents = get_adjacents(grid)
    pickle.dump(adjacents, open("adjacents.p", "wb"))
    maybe_corners = set()
    for a in adjacents:
        print(a, len(adjacents[a]), adjacents[a])
        if len(adjacents[a]) == 2:
            print("maybe corner", a)
            maybe_corners.add(a)
    return maybe_corners


def test_day_twenty():
    grid = parse("Day20sample.txt")
    get_corners(grid)


def day_twenty():
    grid = parse("Day20.txt")
    corners = get_corners(grid)
    if len(corners) == 4:
        ans = 1
        for c in corners:
            ans *= int(c)
        print("ans", ans)


def day_twenty_part_two():
    adjacents = pickle.load(open("adjacents.p", "rb"))
    grid = parse("Day20.txt")
    images = Images(grid, adjacents)
    images.remove_borders()
    monsters, hashes = images.count_sea_monsters()
    print(hashes-15*monsters)


if __name__ == "__main__":
    # test_day_twenty()
    # day_twenty()
    day_twenty_part_two()
