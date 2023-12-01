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


def next_square(cur, facing):
    assert facing in (RIGHT, LEFT, DOWN, UP)
    assert cur in grid

    if facing == RIGHT:
        nxt = (cur[0]+1, cur[1])
        if nxt in grid:
            if grid[nxt] == "#":
                return cur
            return nxt
        else:
            g = cur
            while (g[0]-1, g[1]) in grid:
                g = (g[0]-1, g[1])
            if grid[g] == "#":
                return cur
            return g
    if facing == LEFT:
        nxt = (cur[0]-1, cur[1])
        if nxt in grid:
            if grid[nxt] == "#":
                return cur
            return nxt
        else:
            g = cur
            while (g[0]+1, g[1]) in grid:
                g = (g[0]+1, g[1])
            if grid[g] == "#":
                return cur
            return g
    if facing == DOWN:
        nxt = (cur[0], cur[1]+1)
        if nxt in grid:
            if grid[nxt] == "#":
                return cur
            return nxt
        else:
            g = cur
            while (g[0], g[1]-1) in grid:
                g = (g[0], g[1]-1)
            if grid[g] == "#":
                return cur
            return g
    if facing == UP:
        nxt = (cur[0], cur[1]-1)
        if nxt in grid:
            if grid[nxt] == "#":
                return cur
            return nxt
        else:
            g = cur
            while (g[0], g[1]+1) in grid:
                g = (g[0], g[1]+1)
            if grid[g] == "#":
                return cur
            return g


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
            cur = next_square(cur, facing)
            grid[cur] = facing

row = cur[1]+1
col = cur[0]+1

print(sum([row*1000, col*4, DIRECTIONS.index(facing)]))
