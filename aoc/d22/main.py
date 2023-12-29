import copy


xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
xs = [x.split('~') for x in xs]
xs = [[x.split(',') for x in y] for y in xs]
xs = [[tuple(int(x) for x in y) for y in z] for z in xs]


def do_rectangles_collide(rect1, rect2, consider_z=True):
    overlap_z = (
        (rect1['z'] < rect2['z'] + rect2['depth']) and
        (rect1['z'] + rect1['depth'] > rect2['z'])
    )

    if consider_z and overlap_z and (rect1['id'] in xyc[rect2['id']] or rect2['id'] in xyc[rect1['id']]):
        return True
    overlap_x = (
        (rect1['x'] < rect2['x'] + rect2['width']) and
        (rect1['x'] + rect1['width'] > rect2['x'])
    )

    overlap_y = (
        (rect1['y'] < rect2['y'] + rect2['height']) and
        (rect1['y'] + rect1['height'] > rect2['y'])
    )

    return overlap_x and overlap_y and (not consider_z or overlap_z)


def get_rect(start, end, id):
    sx1, sy1, sz1 = start
    sx2, sy2, sz2 = end
    r1 = {
        'x': sx1,
        'y': sy1,
        'z': sz1,
        'width': sx2-sx1+1,
        'height': sy2-sy1+1,
        'depth': sz2-sz1+1,
        'id': id
    }
    return r1


rs1 = [get_rect(start, end, i) for i, (start, end) in enumerate(xs)]
rs1 = {k: v for k, v in enumerate(rs1)}
xyc = {}
for a in rs1.values():
    xyc[a['id']] = []
    for b in rs1.values():
        if a['id'] == b['id']:
            continue
        if do_rectangles_collide(a, b, consider_z=False):
            xyc[a['id']].append(b['id'])
        else:
            aid = a['id']
            bid = b['id']


def advance(rs, sc=False):
    done = False
    total_moves = set()
    while not done:
        done = True
        i = 0
        while i <= max(rs.keys()):
            if i not in rs:
                i += 1
                continue
            r1 = rs[i]
            r1_done = False
            moves = 0
            while not r1_done:
                r1['z'] -= 1
                if r1['z'] < 0:
                    r1['z'] += 1
                    r1_done = True
                    continue
                for j in xyc[r1['id']]:
                    if j not in rs:
                        continue
                    r2 = rs[j]
                    if do_rectangles_collide(r1, r2):
                        r1['z'] += 1
                        r1_done = True
                        break
                if not r1_done:
                    done = False
                    moves += 1
            if moves > 0:
                total_moves.add(i)
                if sc:
                    return len(total_moves)
            i += 1
    return len(total_moves)


advance(rs1)
can_delete = 0
total = 0
for i in range(len(rs1)):
    c = copy.deepcopy(rs1)
    c.pop(i)
    tm = advance(c)
    total += tm
    print(i, tm)
    if tm == 0:
        can_delete += 1

print(can_delete)
print(total)
