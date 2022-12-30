from collections import deque


def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()


class CombatUnit:
    def __init__(self, what, ap=3):
        self.what = what
        self.hp = 200
        self.ap = ap

    def __repr__(self):
        return self.what

    def __str__(self) -> str:
        return self.what


lines = get_data('input.txt')

# lines = """#######
# #.G...#
# #...EG#
# #.#.#G#
# #..G#E#
# #.....#
# #######
# """
# lines = """#######
# #E..G.#
# #...#.#
# #.G.#G#
# #######"""
# lines = """#########
# #G..G..G#
# #.......#
# #.......#
# #G..E..G#
# #.......#
# #.......#
# #G..G..G#
# #########"""
# lines = """#######
# #.G...#
# #...EG#
# #.#.#G#
# #..G#E#
# #.....#
# #######"""
# lines = """#######
# #G..#E#
# #E#E.E#
# #G.##.#
# #...#E#
# #...E.#
# #######"""
# lines = """#######
# #E..EG#
# #.#G.E#
# #E.##E#
# #G..#.#
# #..E#.#
# ####### """
# lines = """#######
# #E.G#.#
# #.#G..#
# #G.#.G#
# #G..#.#
# #...E.#
# #######"""
# lines = """#########
# #G......#
# #.E.#...#
# #..##..G#
# #...##..#
# #...#...#
# #.G...G.#
# #.....G.#
# #########"""
lines = lines.strip().split('\n')

grid = {}


def move_order():
    return sorted([(k, v) for k, v in grid.items() if type(v) == CombatUnit], key=lambda x: (x[0][1], x[0][0]))


def in_range(target):
    res = []
    for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        r = (target[0]+d[0], target[1]+d[1])
        if r in grid and grid[r] != "#":
            res.append(r)
    return res


def attack(attacker, pos):
    if attacker.hp <= 0:
        return
    targets = []
    for d in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        maybe = (pos[0]+d[0], pos[1]+d[1])
        if maybe in grid and type(grid[maybe]) == CombatUnit:
            cu = grid[maybe]
            if cu.what != attacker.what:
                targets.append((maybe, grid[maybe]))
    targets = sorted(targets, key=lambda x: x[1].hp)
    if len(targets) == 0:
        return
    target = None
    if len(targets) == 1:
        target = targets[0]
    if len(targets) > 1:
        if targets[0][1].hp == targets[1][1].hp:
            targets = targets[:2]
            target = min(targets, key=lambda x: (x[0][1], x[0][0]))
        else:
            target = targets[0]
    target[1].hp -= attacker.ap
    if target[1].hp <= 0:
        grid[target[0]] = "."


def distance_to(start, end):
    assert grid[end] == '.'
    Q = deque()
    Q.append((start, 0))
    seen = set()
    while Q:
        cur, elapsed = Q.popleft()
        if cur == end:
            return (cur, elapsed)
        if cur not in seen:
            for D in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nxt = (cur[0]+D[0], cur[1]+D[1])
                if nxt in grid and grid[nxt] == '.':
                    Q.append(((cur[0]+D[0], cur[1]+D[1]), elapsed+1))
        seen.add(cur)
    return (end, -1)


def choose_next_step(start, end):
    options = []
    for D in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nxt = (start[0]+D[0], start[1]+D[1])
        if grid[nxt] == '.':
            dist = distance_to(nxt, end)
            if dist[1] != -1:
                options.append((dist, nxt))
    assert len(options) > 0
    closest = min(options, key=lambda x: x[0][1])
    closests = [x for x in options if x[0][1] == closest[0][1]]
    return min(closests, key=lambda x: (x[1][1], x[1][0]))[1]


def choose_target(distances):
    distances = [x for x in distances if x[1] != -1]
    if len(distances) == 0:
        return None
    closest = min(distances, key=lambda x: x[1])
    closests = [x for x in distances if x[1] == closest[1]]
    return min(closests, key=lambda x: (x[0][1], x[0][0]))


def move(unit, all_in_range):
    all_in_range = [x for x in all_in_range if grid[x] == "."]
    if len(all_in_range) == 0:
        return unit
    dists = [distance_to(unit[0], x) for x in all_in_range]
    target = choose_target(dists)
    if not target:
        return unit
    target = target[0]

    current = unit[0]
    nxt = choose_next_step(unit[0], target)
    assert grid[nxt] == '.'
    grid[nxt] = unit[1]
    grid[current] = "."
    return nxt, unit[1]


def render():
    s = ""
    for y in range(0, len(lines)):
        for x in range(0, len(lines[y])):
            s += str(grid[(x, y)])
        s += '\n'
    return s


def tick():
    # for each unit:
    units = move_order()
    full_round = True
    for u in units:
        unit_square, unit = u
        targets = [x for x in grid.keys() if type(
            grid[x]) == CombatUnit and grid[x].what != unit.what]
        can_attack = []
        all_in_range = set()
        for target in targets:
            in_range_squares = in_range(target)
            for irs in in_range_squares:
                all_in_range.add(irs)
            if unit_square in in_range_squares:
                can_attack.append(target)

        if len(can_attack) == 0:
            next_pos, unit = move(u, all_in_range)
        else:
            next_pos, unit = u

        attack(unit, next_pos)

        full_round = full_round and len(targets) > 0

    return full_round


def attempt():
    j = 3
    while True:

        for y in range(0, len(lines)):
            for x in range(0, len(lines[y])):
                if lines[y][x] in ("G", "E"):
                    ap = 3 if lines[y][x] == "G" else j
                    grid[(x, y)] = CombatUnit(lines[y][x], ap)
                else:
                    grid[(x, y)] = lines[y][x]
        elves = [x for x in grid.values() if type(
            x) == CombatUnit and x.what == 'E']
        no_elves = len(elves)
        i = 1
        last_round = None
        while True:
            cont = tick()
            if not cont:
                last_round = i-1
            i += 1
            if not cont:
                break

        s = 0
        winner = None
        for v in grid.values():
            if type(v) == CombatUnit:
                s += v.hp
                if not winner:
                    winner = v
        if j == 3:
            print("part one:", last_round*s, winner, j)
        elves = [x for x in grid.values() if type(
            x) == CombatUnit and x.what == 'E']
        still_elves = len(elves)
        if winner.what == 'E' and still_elves == no_elves:
            print("part two:", last_round*s, winner, j)
            break
        else:
            j += 1


attempt()
