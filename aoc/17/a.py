from utilaoc import file_to_strings

def launch(xv, yv, minx, maxx, miny, maxy):
    x = 0
    y = 0
    maxy_obsv = 0
    while True:
        x += xv
        if xv > 0:
            xv -= 1
        elif xv < 0:
            xv += 1
        y += yv
        yv -= 1
        if y > maxy_obsv:
            maxy_obsv = y
        if minx <= x <= maxx and miny <= y <= maxy:
            return (True, maxy_obsv)
        # print(x, y)
        if x > maxx or y < miny:
            return (False, -1)

# print(launch(6, 3, 201, 230, -99, -65))

maxy = 0
for x in range(1, 400):
    for y in range(-400, 400):
        hit, yz = launch(x, y, 201, 230, -99, -65)
        # hit, yz = launch(x, y, 20, 30, -10, -5)
        if hit:
        # if hit and yz > maxy:
        #     maxy = y
            print(x, y)

# python a.py | wc -l # for answer