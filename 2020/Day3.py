from utils import timed

def parse(filename):
    grid = {}
    with open(filename) as f:
        cur_line = 0
        for line in f:
            line = line.strip('\n')
            if cur_line not in grid:
                grid[cur_line] = {}
            for i, pt in enumerate(line):
                grid[cur_line][i] = pt
            cur_line += 1
    return grid

def extend(grid, slope_r, slope_d):
    ht = len(grid)
    orig_w = len(grid[0])
    cur_w = orig_w
    required_w = ht*slope_r*slope_d
    i = 1
    while cur_w < required_w:
        for x in range(ht):
            for y in range(orig_w):
                grid[x][orig_w*i+y] = grid[x][y]
        i += 1
        cur_w = len(grid[0])

    return grid

def print_grid(grid):
    for i in grid:
        line = ""
        for j in grid[i]:
            line += grid[i][j]
        print(line)

def count_trees(grid, slope_r, slope_d):
    cur_x = 0
    cur_y = 0
    ct = 0
    while cur_y in grid and cur_x in grid[cur_y]:
        if grid[cur_y][cur_x] == "#":
            ct += 1
            #print(cur_y, cur_x)
        cur_y += slope_d
        cur_x += slope_r
    return ct

@timed
def test_day_three():
    grid = parse("Day3sample.txt")
    grid = extend(grid, 3, 1)
    #print_grid(grid)
    ct = count_trees(grid, 3, 1)
    assert ct == 7
    
@timed    
def day_three():
    grid = parse("Day3.txt")
    grid = extend(grid, 3, 1)
    ct = count_trees(grid, 3, 1)
    assert 278 == ct

@timed
def test_day_three_part_two():
    """
    Right 1, down 1.
    Right 3, down 1. (This is the slope you already checked.)
    Right 5, down 1.
    Right 7, down 1.
    Right 1, down 2.
    """
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    ct = 1
    for slope in slopes:
        grid = parse("Day3sample.txt")
        grid = extend(grid, slope[0], slope[1])
        ct *= count_trees(grid, slope[0], slope[1])
    
    assert 336 == ct

@timed
def day_three_part_two():
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    ct = 1
    for slope in slopes:
        grid = parse("Day3.txt")
        grid = extend(grid, slope[0], slope[1])
        ct *= count_trees(grid, slope[0], slope[1])
    
    assert ct == 9709761600

if __name__=="__main__":
    test_day_three()
    day_three()
    test_day_three_part_two()
    day_three_part_two()