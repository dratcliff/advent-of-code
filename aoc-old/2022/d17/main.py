def get_data(filename: str):
    with open(filename, 'r') as f:
        return f.read()


class Piece:
    def __init__(self, maxy):
        self.t = None

    # was useful for debugging
    def show(self):
        pass

    def minx(self):
        return min(self.t, key=lambda x: x[0])

    def maxx(self):
        return max(self.t, key=lambda x: x[0])

    def miny(self):
        return min(self.t, key=lambda x: x[1])

    def maxy(self):
        return max(self.t, key=lambda x: x[1])

    def right(self):
        self.t = tuple((x+1, y) for x, y in self.t)

    def left(self):
        self.t = tuple((x-1, y) for x, y in self.t)

    def down(self):
        self.t = tuple((x, y-1) for x, y in self.t)

    def up(self):
        self.t = tuple((x, y+1) for x, y in self.t)


class Wide(Piece):
    def __init__(self, maxy):
        self.t = tuple((x, maxy+3) for x in range(2, 2+4))

    def show(self):
        print("####")

class Plus(Piece):
    def __init__(self, maxy):
        self.t = tuple((x, maxy+3+y)
                       for x, y in ((3, 0), (2, 1), (3, 1), (4, 1), (3, 2)))

    def show(self):
        print(" #\n###\n #")

    def minx(self):
        return self.t[1]


class El(Piece):
    def __init__(self, maxy):
        self.t = tuple((x, maxy+3+y)
                       for x, y in ((2, 0), (3, 0), (4, 0), (4, 1), (4, 2)))

    def show(self):
        print("  #\n  #\n###")

class Block(Piece):
    def __init__(self, maxy):
        self.t = tuple((x, maxy+3+y)
                       for x, y in ((2, 0), (3, 0), (2, 1), (3, 1)))

    def show(self):
        print("##\n##")

class Tall(Piece):
    def __init__(self, maxy):
        self.t = tuple((x, maxy+3+y)
                       for x, y in ((2, 0), (2, 1), (2, 2), (2, 3)))

    def show(self):
        print("#\n#\n#\n#")


def get_piece(idx, maxy):
    i = idx % 5
    if i == 0:
        return Wide(maxy)
    if i == 1:
        return Plus(maxy)
    if i == 2:
        return El(maxy)
    if i == 3:
        return Tall(maxy)
    if i == 4:
        return Block(maxy)


class Chamber:
    def __init__(self, jets):
        self.m = {}
        for i in range(0, 7):
            self.m[(i, -1)] = "-"

        self.maxy = 0
        self.jets = jets
        self.j_idx = 0
        self.rock_ct = 0

    def add_piece(self, p: Piece):
        can_down = True
        while can_down:
            next_jet = self.jets[self.j_idx % len(self.jets)]
            if next_jet == ">":
                if p.maxx()[0] < 6:
                    p.right()
                    collision = any(x in self.m for x in p.t)
                    if collision:
                        p.left()

            elif next_jet == "<":
                if p.minx()[0] > 0:
                    p.left()
                    collision = any(x in self.m for x in p.t)
                    if collision:
                        p.right()
            else:
                raise Exception
            for k in p.t:
                if (k[0], k[1]-1) in self.m:
                    can_down = False
            if can_down:
                p.down()
            self.j_idx += 1
        for pt in p.t:
            self.m[pt] = "#"
        self.maxy = max(p.maxy()[1] + 1, self.maxy)

    def render(self):
        s = ""
        for y in range(self.maxy+10, max(-2, self.maxy-30), -1):
            for x in range(0, 7):
                pt = (x, y)
                if pt in self.m:
                    s += self.m[pt]
                else:
                    s += "."
            s += '\n'
        return s


lines = get_data('input.txt')
lines = lines.strip().split('\n')
jp = [x for x in lines[0]]

chamber = Chamber(jp)
seen = {}
offset = 0
mod = 0
vals = {}

# just storing the renderings to figure out when we've seen a state before
for i in range(0, 10000):
    chamber.add_piece(get_piece(i, chamber.maxy))
    if i == 2021: # 0-index :(
        print("Part one:", chamber.maxy)
    r = chamber.render()
    if r not in seen:
        seen[r] = (i, chamber.maxy, 1)
    else:
        # some renderings repeat before the actual repeating chunk
        # wait until after the chunk size to break
        if seen[r][2] == 2 and seen[r][0] > len(jp)//5:
            mod = len(vals)+1
            break
        if seen[r][2] >= 1 and i > len(jp)//5:
            vals[seen[r][0]] = seen[r][1]
            if offset == 0:
                offset = chamber.maxy-seen[r][1]
        seen[r] = (seen[r][0], seen[r][1], seen[r][2]+1)

height = (((1000000000000-1)//mod))*offset + vals[(((1000000000000-1)%mod))] # 0-index :(
print("Part two:", height)
