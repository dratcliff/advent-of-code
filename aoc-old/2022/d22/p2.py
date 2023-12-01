def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()


lines = get_data('input.txt')
lines = lines.split('\n\n')
board = lines[0]
board = board.split('\n')
moves = lines[1]
moves = moves.replace("R", " R ").replace("L", " L ")
moves = moves.split()
moves = [int(x) if x not in ("L", "R") else x for x in moves]
grid = {}
maxx = 0
maxy = 0

for y in range(0, len(board)):
    if maxy == 0:
        maxy = len(board)
    for x in range(0, len(board[y])):
        if board[y][x] != " ":
            grid[(x, y)] = board[y][x]
        if len(board[y]) > maxx:
            maxx = len(board[y])


def render():
    s = ""
    for y in range(0, maxy):
        for x in range(0, maxx):
            if (x, y) in grid:
                s += grid[(x, y)]
            else:
                s += " "
        s += '\n'
    print(s)


RIGHT, DOWN, LEFT, UP = ">", "v", "<", "^"

EDGE_SIZE = 50

# tip of the hat to the rubik's cube who helped me through this


def cube_me(cur, facing):
    assert facing in (RIGHT, LEFT, UP, DOWN)
    if facing == RIGHT:
        assert (cur[0]+1) % EDGE_SIZE == 0
        if cur[0] == (3*EDGE_SIZE - 1):  # blue right -> yellow left
            x = 2*EDGE_SIZE-1
            y = 3*EDGE_SIZE-1 - (cur[1] % EDGE_SIZE)
            return ((x, y), LEFT)
        elif cur[0] == 2*EDGE_SIZE - 1 and cur[1] >= EDGE_SIZE*2:  # yellow right -> blue left
            x = 3*EDGE_SIZE-1
            y = EDGE_SIZE - 1 - (cur[1] % EDGE_SIZE)
            return ((x, y), LEFT)
        elif cur[0] == 2*EDGE_SIZE - 1 and cur[1] < EDGE_SIZE*2:  # red right -> blue up
            x = cur[1] + EDGE_SIZE
            y = EDGE_SIZE-1
            return ((x, y), UP)
        elif cur[0] < EDGE_SIZE:  # orange right -> yellow up
            x = cur[1] - 2*EDGE_SIZE
            y = 3*EDGE_SIZE - 1
            return ((x, y), UP)
        else:
            raise Exception
    elif facing == LEFT:
        assert (cur[0]) % EDGE_SIZE == 0
        if cur[0] == EDGE_SIZE and cur[1] < EDGE_SIZE:  # white left -> green right, flip y
            x = 0
            y = EDGE_SIZE*3 - 1 - (cur[1] % EDGE_SIZE)
            return ((x, y), RIGHT)
        elif cur[0] == EDGE_SIZE and cur[1] < 2*EDGE_SIZE:  # red left -> green down
            x = cur[1] % EDGE_SIZE
            y = EDGE_SIZE * 2
            return ((x, y), DOWN)
        elif cur[0] == 0 and cur[1] < EDGE_SIZE * 3:  # green left -> white right, flip y
            x = EDGE_SIZE
            y = EDGE_SIZE - 1 - cur[1] % EDGE_SIZE
            return ((x, y), RIGHT)
        elif cur[0] == 0 and cur[1] >= EDGE_SIZE*3:  # orange left -> white down
            x = EDGE_SIZE + cur[1] % EDGE_SIZE
            y = 0
            return ((x, y), DOWN)
        else:
            raise Exception
    elif facing == DOWN:
        assert (cur[1]+1) % EDGE_SIZE == 0
        if cur[0] >= EDGE_SIZE*2:  # blue down -> red left
            x = 2*EDGE_SIZE-1
            y = EDGE_SIZE+cur[0] % EDGE_SIZE
            return ((x, y), LEFT)
        elif cur[0] >= EDGE_SIZE:  # yellow down -> orange left
            x = EDGE_SIZE-1
            y = EDGE_SIZE*3 + cur[0] % EDGE_SIZE
            return ((x, y), LEFT)
        elif cur[0] < EDGE_SIZE:  # orange down -> blue down
            x = EDGE_SIZE*2 + cur[0] % EDGE_SIZE
            y = 0
            return ((x, y), DOWN)
        else:
            raise Exception
    elif facing == UP:
        assert (cur[1]) % EDGE_SIZE == 0
        if cur[1] == 0 and cur[0] >= EDGE_SIZE*2:  # blue up -> orange up
            y = 4*EDGE_SIZE-1
            x = cur[0] % EDGE_SIZE
            return ((x, y), UP)
        elif cur[1] == 0 and cur[0] >= EDGE_SIZE:  # white up -> orange right
            x = 0
            y = 3*EDGE_SIZE + (cur[0] % EDGE_SIZE)
            return ((x, y), RIGHT)
        elif cur[1] == 2*EDGE_SIZE:  # green up -> red right
            x = EDGE_SIZE
            y = EDGE_SIZE + cur[0] % EDGE_SIZE
            return ((x, y), RIGHT)
        else:
            raise Exception
    else:
        raise Exception(facing, cur)


def next_square(cur, facing):
    assert facing in (RIGHT, LEFT, DOWN, UP)
    assert cur in grid
    if facing == RIGHT:
        nxt = (cur[0]+1, cur[1])
        if nxt in grid:
            if grid[nxt] == "#":
                return cur, facing
            return nxt, facing
        else:
            g, new_facing = cube_me(cur, facing)
            assert g in grid
            if grid[g] == "#":
                return cur, facing
            return g, new_facing
    if facing == LEFT:
        nxt = (cur[0]-1, cur[1])
        if nxt in grid:
            if grid[nxt] == "#":
                return cur, facing
            return nxt, facing
        else:
            g, new_facing = cube_me(cur, facing)
            assert g in grid
            if grid[g] == "#":
                return cur, facing
            return g, new_facing
    if facing == DOWN:
        nxt = (cur[0], cur[1]+1)
        if nxt in grid:
            if grid[nxt] == "#":
                return cur, facing
            return nxt, facing
        else:
            g, new_facing = cube_me(cur, facing)
            assert g in grid
            if grid[g] == "#":
                return cur, facing
            return g, new_facing
    if facing == UP:
        nxt = (cur[0], cur[1]-1)
        if nxt in grid:
            if grid[nxt] == "#":
                return cur, facing
            return nxt, facing
        else:
            g, new_facing = cube_me(cur, facing)
            assert g in grid
            if grid[g] == "#":
                return cur, facing
            return g, new_facing


starting_pos = [(k[0], k[1])
                for k, v in grid.items() if k[1] == 0 and v == "."][0]
cur = starting_pos
DIRECTIONS = [RIGHT, DOWN, LEFT, UP]
facing = RIGHT

for move in moves:
    if move in ("R", "L"):
        i = 1 if move == "R" else -1
        facing = DIRECTIONS[(DIRECTIONS.index(facing)+i) % len(DIRECTIONS)]
    else:
        for i in range(0, move):
            grid[cur] = facing
            cur, facing = next_square(cur, facing)
            assert cur in grid
            grid[cur] = facing
    row = cur[1]+1
    col = cur[0]+1

row = cur[1]+1
col = cur[0]+1
print(sum([row*1000, col*4, DIRECTIONS.index(facing)]))

# t2.txt modified to match input.txt so I'd have something to test with.
# I found a really neat, general way to make any unfolded cube match
# this configuration, but the algorithm was too large to fit in this
# margin.