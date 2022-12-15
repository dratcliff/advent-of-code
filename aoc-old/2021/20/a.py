from utilaoc import file_to_strings, file_to_grid

algo = file_to_strings("a.txt")[0]
algo = [1 if x == "#" else 0 for x in algo]
input_img = file_to_grid("a2.txt")

offsets = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (0, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]

minx = 0
maxx = 0
miny = 0
maxy = 0

for k in input_img:
    if k[0] > maxx:
        maxx = k[0]
    if k[1] > maxy:
        maxy = k[1]


def pixel_number(pixel, g, odd):
    number = ""
    for i in range(0, len(offsets)):
        cp = (pixel[0]+offsets[i][0], pixel[1]+offsets[i][1])
        if cp in g:
            if g[cp] == "#":
                number += "1"
            else:
                number += "0"
        else:
            if odd:
                number += "1"
            else:
                number += "0"
    return int(number, 2)


def next_img(g, odd):
    global minx, miny, maxx, maxy
    if odd:
        s = "#"
    else:
        s = "."
    for i in range(minx, maxx+1):
        for j in range(1, 5):
            g[(i, miny-j)] = s
            g[(i, maxy+j)] = s

    miny -= 4
    maxy += 4

    for i in range(miny, maxy+1):
        for j in range(1, 5):
            g[(minx-j, i)] = s
            g[(maxx+j, i)] = s

    minx -= 4
    maxx += 4

    img = {}
    for pixel in g:
        pn = pixel_number(pixel, g, odd)
        algo_number = algo[pn]
        if algo_number == 1:
            img[pixel] = "#"
        else:
            img[pixel] = '.'

    return img


def run():
    g = input_img
    for i in range(0, 50):
        odd = algo[0] == 1 and algo[511] == 0 and i % 2 != 0
        g = next_img(g, odd)
        c = 0
        for v in g.values():
            if v == '#':
                c += 1
        print(i, c)


run()
