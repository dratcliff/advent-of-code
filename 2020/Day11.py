
class Grid:
    def __init__(self, seats, row_len, change_ct, visible):
        self.seats = seats
        self.row_len = row_len
        self.change_ct = change_ct
        self.visible = visible

    def get_visible(self):
        if self.visible:
            return self.visible
        else:
            visible = {}
            for i in range(0, len(self.seats)):
                visible[i] = {}
                for j in range(0, self.row_len):
                    if j in self.seats[i]:
                        if j not in visible[i]:
                            visible[i][j] = []
                        # left
                        k = 1
                        left = j-k in self.seats[i]
                        while j-k >= 0 and not left:
                            k += 1
                            left = j-k in self.seats[i]
                        if left:
                            visible[i][j].append((i, j-k))
                        # right
                        k = 1
                        right = j+k in self.seats[i]
                        while j+k < self.row_len and not right:
                            k += 1
                            right = j+k in self.seats[i]
                        if right:
                            visible[i][j].append((i, j+k))
                        # up
                        k = 1
                        up = i-k in self.seats and j in self.seats[i-k]
                        while i-k >= 0 and not up:
                            k += 1
                            up = i-k in self.seats and j in self.seats[i-k]
                        if up:
                            visible[i][j].append((i-k, j))
                        # down
                        k = 1
                        down = i+k in self.seats and j in self.seats[i+k]
                        while i+k < len(self.seats) and not down:
                            k += 1
                            down = i+k in self.seats and j in self.seats[i+k]
                        if down:
                            visible[i][j].append((i+k, j))
                        # up-left
                        k = 1
                        up_left = i-k in self.seats and j-k in self.seats[i-k]
                        while i-k >= 0 and j-k >= 0 and not up_left:
                            k += 1
                            up_left = i-k in self.seats and j-k in self.seats[i-k]
                        if up_left:
                            visible[i][j].append((i-k, j-k))
                        # up-right
                        k = 1
                        up_right = i-k in self.seats and j+k in self.seats[i-k]
                        while i-k >= 0 and j+k < self.row_len and not up_right:
                            k += 1
                            up_right = i-k in self.seats and j+k in self.seats[i-k]
                        if up_right:
                            visible[i][j].append((i-k, j+k))
                        # down-left
                        k = 1
                        down_left = i+k in self.seats and j-k in self.seats[i+k]
                        while i+k < len(self.seats) and j-k >= 0 and not down_left:
                            k += 1
                            down_left = i+k in self.seats and j-k in self.seats[i+k]
                        if down_left:
                            visible[i][j].append((i+k, j-k))
                        # down-right
                        k = 1
                        down_right = i+k in self.seats and j+k in self.seats[i+k]
                        while i+k < len(self.seats) and j+k < self.row_len and not down_right:
                            k += 1
                            down_right = i+k in self.seats and j+k in self.seats[i+k]
                        if down_right:
                            visible[i][j].append((i+k, j+k))

            self.visible = visible
        return self.visible


def parse(filename):
    seats = {}
    row_len = 0
    with open(filename) as f:
        for i, line in enumerate(f):
            line = line.strip('\n')
            if row_len == 0:
                row_len = len(line)
            seats[i] = {}
            for j, c in enumerate(line):
                if c != ".":
                    seats[i][j] = False
    return Grid(seats, row_len, len(seats)*row_len, None)

def render(g):
    seats = g.seats
    row = ""
    for i in range(0, len(seats)):
        for j in range(0, g.row_len):
            if j in seats[i]:
                s = seats[i][j]
                if s:
                    row += "#"
                else:
                    row += "L"
            else:
                row += "."
        row += '\n'
    print(row)

def tick(g):
    """If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    Otherwise, the seat's state does not change."""
    ng = {}
    seats = g.seats
    rlen = g.row_len
    change_ct = 0
    for i in range(0, len(seats)):
        ng[i] = {}
        for j in range(0, rlen):
            if j in seats[i]:
                adj_ct = 0
                if i-1 in seats:
                    above = seats[i-1]
                    if j-1 in above:
                        if above[j-1]:
                            adj_ct += 1
                    if j in above:
                        if above[j]:
                            adj_ct += 1
                    if j+1 in above:
                        if above[j+1]:
                            adj_ct += 1
                if i+1 in seats:
                    below = seats[i+1]
                    if j-1 in below:
                        if below[j-1]:
                            adj_ct += 1
                    if j in below:
                        if below[j]:
                            adj_ct += 1
                    if j+1 in below:
                        if below[j+1]:
                            adj_ct += 1
                if j-1 in seats[i]:
                    if seats[i][j-1]:
                        adj_ct += 1
                if j+1 in seats[i]:    
                    if seats[i][j+1]:
                        adj_ct += 1
                if seats[i][j] and adj_ct >= 4:
                    ng[i][j] = False
                    change_ct += 1
                elif not seats[i][j] and adj_ct == 0:
                    ng[i][j] = True
                    change_ct += 1
                else:
                    ng[i][j] = seats[i][j]
    return Grid(ng, rlen, change_ct, None)

def tick2(g):
    """
    Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to 
    become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, 
    seats matching no rule don't change, and floor never changes."""
    ng = {}
    seats = g.seats
    rlen = g.row_len
    change_ct = 0
    for i in range(0, len(seats)):
        ng[i] = {}
        for j in range(0, rlen):
            if j in seats[i]:
                adj_ct = 0
                for v in g.get_visible()[i][j]:
                    if seats[v[0]][v[1]]:
                        adj_ct += 1
                if seats[i][j] and adj_ct >= 5:
                    ng[i][j] = False
                    change_ct += 1
                elif not seats[i][j] and adj_ct == 0:
                    ng[i][j] = True
                    change_ct += 1
                else:
                    ng[i][j] = seats[i][j]
    return Grid(ng, rlen, change_ct, g.get_visible())

def count_occupied(g):
    ct = 0
    for r in g.seats.values():
        ct += sum(1 for x in r.values() if x)
    return ct

def test_day_eleven():
    g = parse("Day11sample.txt")
    while g.change_ct != 0:
        g = tick(g)
    
    occ_ct = count_occupied(g)
    assert 37 == occ_ct

def day_eleven():
    g = parse("Day11.txt")
    while g.change_ct != 0:
        g = tick(g)
    
    occ_ct = count_occupied(g)
    assert 2481 == occ_ct

def test_day_eleven_part_two():
    g = parse("Day11sample.txt")
    while g.change_ct != 0:
        g = tick2(g)
    occ_ct = count_occupied(g)
    assert 26 == occ_ct

def day_eleven_part_two():
    g = parse("Day11.txt")
    while g.change_ct != 0:
        g = tick2(g)
    occ_ct = count_occupied(g)
    assert 2227 == occ_ct

def run():
    import time
    g = parse("Day11.txt")
    render(g)
    while g.change_ct != 0:
        g = tick2(g)
        time.sleep(.1)
        print('\033c')
        render(g)

if __name__=="__main__":
    test_day_eleven()
    day_eleven()
    test_day_eleven_part_two()
    day_eleven_part_two()
    run()