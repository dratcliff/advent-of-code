from collections import namedtuple
D = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}
xs = [x.strip('\n') for x in open('input.txt', 'r').readlines()]
xs = [x.split()[2] for x in xs]
xs = [(D[x[7]], int(x[2:7], 16)) for x in xs]


# fd = front driver, rp = rear passenger, etc
Car = namedtuple("Car", ["fd", "fp", "rd", "rp"])


def rotate_right(car):
    return Car(car.fp, car.rp, car.fd, car.rd)


def rotate_left(car):
    return Car(car.rd, car.fd, car.rp, car.fp)


# print(xs)


DV = [] # vertices experienced by "driver's side"
PV = [] # vertices experienced by "passenger's side"
cur = Car((0, 0), (1, 0), (0, 1), (1, 1))

for i in range(len(xs)):
    dir, dist = xs[i]
    last_dir, last_dist = 'U', -0
    if i > 0:
        last_dir, last_dist = xs[i-1]
    shift = None

    match dir:
        case 'R':
            if last_dir == 'U':
                DV.append(cur.fd)
                cur = rotate_right(cur)
                PV.append(cur.fd)
            else:
                PV.append(cur.fd)
                cur = rotate_left(cur)
                DV.append(cur.fd)
            shift = (1, 0)
        case 'L':
            if last_dir == 'U':
                PV.append(cur.fd)
                cur = rotate_left(cur)
                DV.append(cur.fd)
            else:
                DV.append(cur.fd)
                cur = rotate_right(cur)
                PV.append(cur.fd)
            shift = (-1, 0)
        case 'D':
            if last_dir == 'L':
                PV.append(cur.fd)
                cur = rotate_left(cur)
                DV.append(cur.fd)
            elif last_dir == 'R':
                DV.append(cur.fd)
                cur = rotate_right(cur)
                PV.append(cur.fd)
            shift = (0, 1)
        case 'U':
            if last_dir == 'L':
                DV.append(cur.fd)
                cur = rotate_right(cur)
                PV.append(cur.fd)
            elif last_dir == 'R':
                PV.append(cur.fd)
                cur = rotate_left(cur)
                DV.append(cur.fd)
            shift = (0, -1)
    cur = Car(*[(x[0]+shift[0]*dist, x[1]+shift[1]*dist) for x in cur])


# thanks, chatgpt
def polygon_area(vertices):
    n = len(vertices)
    if n < 3:
        raise ValueError("A polygon must have at least 3 vertices.")

    area = 0.0
    for i in range(n - 1):
        area += vertices[i][0] * vertices[i + 1][1]
        area -= vertices[i + 1][0] * vertices[i][1]

    # Add contribution from the last edge
    area += vertices[n - 1][0] * vertices[0][1]
    area -= vertices[0][0] * vertices[n - 1][1]

    # Take the absolute value and divide by 2
    area = abs(area) / 2.0

    return int(area)


print(max(polygon_area(DV), polygon_area(PV)))
